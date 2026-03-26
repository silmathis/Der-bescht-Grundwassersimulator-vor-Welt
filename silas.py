from pathlib import Path

import matplotlib.pyplot as plt


def plot_quadratic(a: float, b: float, c: float, filename: str = "quadratische_funktion.png") -> Path:
	"""Plot y = ax^2 + bx + c and save it as an image in the plots folder."""
	x_values = [x / 10 for x in range(-100, 101)]
	y_values = [a * x**2 + b * x + c for x in x_values]

	output_dir = Path("plots")
	output_dir.mkdir(exist_ok=True)
	output_path = output_dir / filename

	plt.figure(figsize=(8, 5))
	plt.plot(x_values, y_values, label=f"y = {a}x^2 + {b}x + {c}", color="blue")
	plt.axhline(0, color="black", linewidth=0.8)
	plt.axvline(0, color="black", linewidth=0.8)
	plt.grid(True, linestyle="--", alpha=0.6)
	plt.title("Quadratische Funktion")
	plt.xlabel("x")
	plt.ylabel("y")
	plt.legend()
	plt.tight_layout()
	plt.savefig(output_path, dpi=150)
	plt.close()

	return output_path


if __name__ == "__main__":
	saved_file = plot_quadratic(a=1, b=0, c=0)
	print(f"Plot gespeichert unter: {saved_file.resolve()}")
