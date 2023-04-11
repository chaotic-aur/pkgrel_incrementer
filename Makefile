pkgrel_incrementer.sif:
	singularity build --fakeroot "$@" Singularity

clean:
	rm -f pkgrel_incrementer.sif
