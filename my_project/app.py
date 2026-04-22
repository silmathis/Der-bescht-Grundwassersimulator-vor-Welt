"""
Interactive 2D Groundwater Flow Simulator - Streamlit Application

This is an educational tool for exploring how hydraulic conductivity, 
recharge, and subsurface structure influence groundwater flow patterns.

WARNING: This is a simplified educational model, not suitable for 
engineering predictions or real-world applications.
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from my_project.groundwater_model import GroundwaterModel

# Page config
st.set_page_config(
    page_title="Groundwater Flow Simulator",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and warning
st.title("Interactive Groundwater Flow Simulator")
st.markdown("""
**Educational Tool Only**  
This is a simplified, conceptual model designed for learning and exploration.
It is **not** suitable for engineering predictions or real-world applications.
""")

# Initialize session state
if 'model' not in st.session_state:
    st.session_state.model = GroundwaterModel(nx=60, ny=40)
    st.session_state.solved = False
    st.session_state.previous_model = None

model = st.session_state.model

# ============================================================================
# SIDEBAR: PARAMETER CONTROLS
# ============================================================================

st.sidebar.header("Model Parameters")

# Grid size
st.sidebar.subheader("Domain Size")
nx = st.sidebar.slider(
    "Grid width (cells)",
    min_value=20, max_value=100, value=model.nx,
    help="Horizontal grid resolution"
)
ny = st.sidebar.slider(
    "Grid height (cells)",
    min_value=15, max_value=80, value=model.ny,
    help="Vertical grid resolution"
)

if nx != model.nx or ny != model.ny:
    st.session_state.model = GroundwaterModel(nx=nx, ny=ny)
    st.session_state.solved = False
    model = st.session_state.model
    st.rerun()

# Boundary conditions
st.sidebar.subheader("Boundary Conditions (Head in meters)")
col1, col2 = st.sidebar.columns(2)
with col1:
    head_north = st.slider("North (top)", 0.0, 30.0, 15.0, step=0.5)
    head_south = st.slider("South (bottom)", 0.0, 30.0, 5.0, step=0.5)
with col2:
    head_west = st.slider("West (left)", 0.0, 30.0, 10.0, step=0.5)
    head_east = st.slider("East (right)", 0.0, 30.0, 10.0, step=0.5)

st.sidebar.info(
    "**Tip:** Higher boundary values at the top will drive flow downward."
)

# Zone definitions
st.sidebar.subheader("Subsurface Zones")
st.sidebar.markdown("""
Define zones with different hydraulic conductivity (permeability).
""")

zone_type = st.sidebar.radio(
    "Add/modify zone:",
    ["High conductivity (sand)", "Low conductivity (clay)", "Medium (silt)"]
)

zone_conductivities = {
    "High conductivity (sand)": 5.0,
    "Low conductivity (clay)": 0.1,
    "Medium (silt)": 1.0
}
selected_k = zone_conductivities[zone_type]

background_k = st.sidebar.slider(
    "Background conductivity K (m/day)",
    min_value=0.1,
    max_value=5.0,
    value=1.0,
    step=0.1,
    help="Base conductivity outside the selected zone"
)

# Zone positioning
col1, col2 = st.sidebar.columns(2)
with col1:
    zone_x_min = st.number_input("X start", 0, nx - 1, value=int(nx * 0.2))
    zone_y_min = st.number_input("Y start", 0, ny - 1, value=int(ny * 0.3))
with col2:
    zone_x_max = st.number_input("X end", 1, nx, value=int(nx * 0.8))
    zone_y_max = st.number_input("Y end", 1, ny, value=int(ny * 0.7))

st.sidebar.caption("The zone is applied when you solve the model.")

# Recharge
st.sidebar.subheader("Recharge (Infiltration)")
recharge_rate = st.sidebar.slider(
    "Recharge rate (m/day)",
    0.0, 0.05, 0.01, step=0.001,
    help="Rainfall or infiltration added from above"
)
recharge_x_min = st.sidebar.number_input("R: X start", 0, nx - 1, value=int(nx * 0.3), key="rechg_x_min")
recharge_x_max = st.sidebar.number_input("R: X end", 1, nx, value=int(nx * 0.7), key="rechg_x_max")
recharge_y_min = st.sidebar.number_input("R: Y start", 0, ny - 1, value=int(ny * 0.1), key="rechg_y_min")
recharge_y_max = st.sidebar.number_input("R: Y end", 1, ny, value=int(ny * 0.3), key="rechg_y_max")

st.sidebar.caption("Recharge is applied when you solve the model.")

# Reset button
if st.sidebar.button("Reset Model", type="secondary"):
    st.session_state.model = GroundwaterModel(nx=nx, ny=ny)
    st.session_state.solved = False
    st.rerun()

# Solver controls
st.sidebar.subheader("Solver")
iterations = st.sidebar.slider("Max iterations", 10, 500, 100)
tolerance = st.sidebar.selectbox(
    "Convergence tolerance",
    [1e-2, 1e-3, 1e-4, 1e-5],
    format_func=lambda x: f"{x:.0e}"
)

current_controls = (
    nx,
    ny,
    head_north,
    head_south,
    head_west,
    head_east,
    zone_type,
    zone_x_min,
    zone_x_max,
    zone_y_min,
    zone_y_max,
    background_k,
    selected_k,
    recharge_rate,
    recharge_x_min,
    recharge_x_max,
    recharge_y_min,
    recharge_y_max,
    iterations,
    tolerance,
)

if st.session_state.get("last_controls") != current_controls:
    st.session_state.solved = False
    st.session_state.last_controls = current_controls

# ============================================================================
# MAIN PANEL: SOLVE AND VISUALIZE
# ============================================================================

col_main, col_info = st.columns([3, 1])

with col_main:
    if st.button("Solve Model", use_container_width=True, type="primary"):
        with st.spinner("Solving..."):
            st.session_state.previous_model = st.session_state.model
            solved_model = GroundwaterModel(nx=nx, ny=ny)
            solved_model.head_north = head_north
            solved_model.head_south = head_south
            solved_model.head_west = head_west
            solved_model.head_east = head_east
            solved_model.set_background_conductivity(background_k)
            solved_model.set_zone(zone_x_min, zone_x_max, zone_y_min, zone_y_max, selected_k)
            solved_model.set_recharge(recharge_x_min, recharge_x_max, recharge_y_min, recharge_y_max, recharge_rate)
            solved_model.solve(iterations=iterations, tolerance=tolerance)
            st.session_state.model = solved_model
            model = solved_model
            st.session_state.solved = True
        st.success("Model solved!")

if st.session_state.solved:
    # Compute flow field
    qx, qy, q_mag = model.compute_flow()
    previous_model = st.session_state.get("previous_model")
    has_previous = (
        previous_model is not None
        and previous_model.head.shape == model.head.shape
    )
    
    with col_info:
        st.subheader("Results")
        summary = model.get_summary()
        st.metric("Head (min)", f"{summary['head_min']:.2f} m")
        st.metric("Head (max)", f"{summary['head_max']:.2f} m")
        st.metric("Flow (max)", f"{summary['flow_max']:.3f} m/day")
    
    # Create visualizations
    tabs = st.tabs([
        "Hydraulic Head",
        "Conductivity",
        "Flow Magnitude",
        "Flow Vectors",
        "Change vs Previous Solve",
    ])
    
    # Tab 1: Hydraulic Head
    with tabs[0]:
        fig_head = go.Figure(data=go.Contour(
            z=model.head,
            colorscale='Viridis',
            colorbar=dict(title="Head (m)"),
            contours=dict(coloring='heatmap')
        ))
        fig_head.update_layout(
            title="Hydraulic Head Distribution",
            xaxis_title="X (cells)",
            yaxis_title="Y (cells)",
            height=500
        )
        st.plotly_chart(fig_head, use_container_width=True)
        st.caption("Higher values = higher hydraulic head. Water flows from high to low head.")
    
    # Tab 2: Conductivity zones
    with tabs[1]:
        col_k1, col_k2 = st.columns(2)
        with col_k1:
            st.metric("K min", f"{float(np.min(model.hydraulic_conductivity)):.2f} m/day")
        with col_k2:
            st.metric("K max", f"{float(np.max(model.hydraulic_conductivity)):.2f} m/day")

        fig_cond = go.Figure(data=go.Heatmap(
            z=np.log10(model.hydraulic_conductivity),
            colorscale='RdYlBu_r',
            colorbar=dict(title="log₁₀(K)")
        ))
        fig_cond.update_layout(
            title="Hydraulic Conductivity (log scale)",
            xaxis_title="X (cells)",
            yaxis_title="Y (cells)",
            height=500
        )
        st.plotly_chart(fig_cond, use_container_width=True)
        st.caption(
            "Red = high permeability (sand), Blue = low permeability (clay). "
            "This plot only changes when zone settings change."
        )
    
    # Tab 3: Flow magnitude
    with tabs[2]:
        fig_mag = go.Figure(data=go.Contour(
            z=q_mag,
            colorscale='Plasma',
            colorbar=dict(title="Flow (m/day)"),
            contours=dict(coloring='heatmap')
        ))
        fig_mag.update_layout(
            title="Groundwater Flow Magnitude",
            xaxis_title="X (cells)",
            yaxis_title="Y (cells)",
            height=500
        )
        st.plotly_chart(fig_mag, use_container_width=True)
        st.caption("Bright = faster flow. Flow follows Darcy's law: q = -K × ∇h")
    
    # Tab 4: Flow vectors
    with tabs[3]:
        # Create magnitude heatmap as background
        fig_vec = go.Figure(data=go.Heatmap(
            z=q_mag,
            colorscale='Blues',
            colorbar=dict(title="Flow (m/day)"),
            name='Flow Magnitude'
        ))
        
        # Add streamlines effect using sparse quiver
        step = max(1, max(model.nx, model.ny) // 12)
        for i in range(0, model.ny, step):
            for j in range(0, model.nx, step):
                if q_mag[i, j] > 1e-6:  # Only show significant flow
                    scale_factor = 3.0
                    fig_vec.add_annotation(
                        x=j, y=i,
                        ax=j - qx[i, j] * scale_factor,
                        ay=i - qy[i, j] * scale_factor,
                        arrowhead=2, arrowsize=1.5,
                        arrowwidth=2, arrowcolor='darkred',
                        xref='x', yref='y',
                        axref='x', ayref='y',
                        showarrow=True
                    )
        
        fig_vec.update_layout(
            title="Flow Direction (Vectors) and Magnitude (Heatmap)",
            xaxis_title="X (cells)",
            yaxis_title="Y (cells)",
            height=500
        )
        st.plotly_chart(fig_vec, use_container_width=True)
        st.caption("Red arrows show flow direction and speed. Blue background shows flow magnitude.")

    # Tab 5: Change compared to previous solution
    with tabs[4]:
        if has_previous:
            prev_qx, prev_qy, prev_q_mag = previous_model.compute_flow()
            head_delta = model.head - previous_model.head
            flow_delta = q_mag - prev_q_mag

            col_delta_1, col_delta_2 = st.columns(2)
            with col_delta_1:
                st.metric("max |Δhead|", f"{np.max(np.abs(head_delta)):.3f} m")
            with col_delta_2:
                st.metric("max |Δflow|", f"{np.max(np.abs(flow_delta)):.3f} m/day")

            fig_head_delta = go.Figure(data=go.Heatmap(
                z=head_delta,
                colorscale='RdBu',
                zmid=0.0,
                colorbar=dict(title="Δhead (m)")
            ))
            fig_head_delta.update_layout(
                title="Head Change Since Previous Solve",
                xaxis_title="X (cells)",
                yaxis_title="Y (cells)",
                height=450
            )
            st.plotly_chart(fig_head_delta, use_container_width=True)

            fig_flow_delta = go.Figure(data=go.Heatmap(
                z=flow_delta,
                colorscale='RdBu',
                zmid=0.0,
                colorbar=dict(title="Δflow (m/day)")
            ))
            fig_flow_delta.update_layout(
                title="Flow-Magnitude Change Since Previous Solve",
                xaxis_title="X (cells)",
                yaxis_title="Y (cells)",
                height=450
            )
            st.plotly_chart(fig_flow_delta, use_container_width=True)
        else:
            st.info("Solve at least twice with different inputs to see change maps.")

# ============================================================================
# FOOTER: HELP AND EXPLANATION
# ============================================================================

st.divider()

with st.expander("How to use this simulator"):
    st.markdown("""
    ### Getting Started
    
    1. **Set Boundary Conditions:** Use the top sliders to set water table heights at domain edges
    2. **Define Zones:** Draw subsurface regions with different rock types (conductivity)
    3. **Add Recharge:** Set where water infiltrates from above
    4. **Solve:** Click "Solve Model" to calculate the flow pattern
    
    ### What do the visualizations show?
    
    - **Hydraulic Head:** The water table elevation. Contour lines show equipotential surfaces.
    - **Conductivity:** Different rock types have different permeability (how easily water flows).
    - **Flow Magnitude:** How fast water moves. Bright colors = faster flow.
    - **Flow Vectors:** Direction and speed of groundwater movement.
    
    ### Key Principles
    
    - **Darcy's Law:** q = -K × ∇h (flow is proportional to conductivity and head gradient)
    - **Flow Direction:** Always from high head → low head
    - **Conductivity Effect:** Higher K (sand) → faster flow; Lower K (clay) → slower flow
    """)

with st.expander("Model Limitations"):
    st.markdown("""
    - **Steady-state only:** This model shows equilibrium, not transient dynamics
    - **Simplified physics:** Uses basic Darcy's law, ignores anisotropy and dispersion
    - **2D only:** Does not represent 3D effects
    - **No wells or rivers:** Simplified boundary conditions
    - **No unsaturated zone:** Water is always saturated (stretch goal)
    - **For learning only:** Do NOT use for engineering decisions or site predictions
    
    This tool is best used to build intuition about how conductivity and recharge affect flow patterns.
    """)

st.sidebar.markdown("---")
st.sidebar.info(
    "**Educational Groundwater Simulator**  \n"
    "Version 0.1.0  \n"
    "Built with Streamlit, NumPy, and SciPy"
)
