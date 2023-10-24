
clean:
	rm -f ../out/*.*

define pdfbuild
	lualatex \
	-shell-escape \
	-file-line-error \
	-interaction=nonstopmode \
	-synctex=1 \
	-output-format=pdf \
	"-output-directory=C:\GitHub\masters-thesis\out" \
	main.tex
endef

define bibtexbuild
	cd ../out; \
	bibtex \
	main
endef

quick:
	echo cat
	echo $(pdfbuild)
	$(pdfbuild)

final:
	rm -f ../out/*.*
	$(pdfbuild)
	$(bibtexbuild)
	$(pdfbuild)
	$(pdfbuild)

