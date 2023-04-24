# learners-permit

## file structure (still being updated)
Learner's Permit file structure is roughly organized like this:
```
├── learners-permit
│   ├── assets
│   ├── data
│   ├── models
```

Where all main source files are under the outer `learners-permit` folder, pictures and graphics are under assets, collected and inputted data are under data, and associated machine learning models are under models.

## running the code
To run the code, navigate to the root directory and run
```
python3 learner-permit.py
```

Note if you need to import dependencies, you may need to install pygame

## code structure
The navigation and menu logic lies in `learner-permit.py`. This file imports from `car-game.py` and its different variants. We have a variant of the `CarGame` class for each of the different game, prediction, playback, and generate modes of the game. 
