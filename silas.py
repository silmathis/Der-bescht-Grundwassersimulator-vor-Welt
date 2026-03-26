from pathlib import Path

import matplotlib.pyplot as plt


def plot_cubic(a: float, b: float, c: float, d: float, filename: str = "kubische_funktion.png") -> Path:
	"""Plot y = ax^3 + bx^2 + cx + d and save it as an image in the plots folder."""
	x_values = [x / 10 for x in range(-100, 101)]
	y_values = [a * x**3 + b * x**2 + c * x + d for x in x_values]

	output_dir = Path("plots")
	output_dir.mkdir(exist_ok=True)
	output_path = output_dir / filename

	plt.figure(figsize=(8, 5))
	plt.plot(x_values, y_values, label=f"y = {a}x^3 + {b}x^2 + {c}x + {d}", color="blue")
	plt.axhline(0, color="black", linewidth=0.8)
	plt.axvline(0, color="black", linewidth=0.8)
	plt.grid(True, linestyle="--", alpha=0.6)
	plt.title("Kubische Funktion")
	plt.xlabel("x")
	plt.ylabel("y")
	plt.legend()
	plt.tight_layout()
	plt.savefig(output_path, dpi=150)
	plt.close()

	return output_path


if __name__ == "__main__":
	saved_file = plot_cubic(a=1, b=0, c=0, d=0)
	print(f"Plot gespeichert unter: {saved_file.resolve()}")
