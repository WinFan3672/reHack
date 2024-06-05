nuitka:
	nuitka3 --onefile rehack.py \
		--output-dir=bin/ \
		--remove-output  \
		--include-data-dir=data=data \
		--include-data-dir=websites=websites \
		--include-data-dir=onionsites=onionsites \
		--include-data-dir=wikis=wikis \
		--include-data-dir=msgboard=msgboard \
		--product-name="reHack" \
		--run \;
clean:
	-rm -r bin/
