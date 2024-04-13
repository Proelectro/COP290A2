
m = "commit"

run:
	python main.py
git:
	git pull origin main
	git add .
	git commit -m "$m"
	git push origin main
	
