# FAMILY TREE

Family-Tree is a Family History Graph Application.

## Getting Started

### Installing requirements

```pip install -r requirements.txt```

### Data Pipeline

Add data to the files listed below:

```/data/people.csv``` for people details

```/data/relations.csv```  for child to parent relationship mapping

### Starting the application
To run the application locally, run the following command:
```
flask run --debug
```
Access from the browser using ```http://127.0.0.1:5000```

### Visualize the relationships

HomePage lists all members in the family tree.
![alt text](https://user-images.githubusercontent.com/49183352/246207649-23c4afad-e0d6-4a33-878e-b1fb310a9c6f.png)

Click the #ID for a member to visualize their family tree.
![alt text](https://user-images.githubusercontent.com/49183352/246207652-dfe54229-096c-47bc-892b-23f020138dbc.png)