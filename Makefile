run:
	python main.py
git:
	git pull origin main
	git add .
	git commit -m $(message)
	git push origin main
	
