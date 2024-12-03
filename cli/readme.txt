>> INSTALLING se2121 (interoperability operator cli app)

In Unix based OSs: 
Run: ./install (in the source directory)

Else:
1. Install python3 if not installed. 
2. Assuming you are in the directory where the source code (cli.py) is 
3. Run: python3 -m venv .env                          #Create a virtual environment to install dependencies
4. Run: . .env/bin/activate 
5. Run: pip install -e .                              #Don't forget the dot: .
6. Run: deactivate


>> RUNNING se2121

In Unix based OSs:
1. Run: . cli (or: source cli)
2. Use as you wish
3. When done: CTRL+C

Else:
1. Run: . .env/bin/activate 
2. Use as you wish (run: se2121 for help)
3. When done, run: deactivate


