test:
	pytest --benchmark-skip

perf:
	pytest --benchmark-only --benchmark-compare
