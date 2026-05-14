# Step 1: Import Libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
from joblib import dump

# Step 2: Load CSV
data = pd.read_csv(r"C:\Users\shahi\Downloads\Autism st\AUTISM_DETECTION\AUTISM_DETECTION\Autism_Screening_Data_Combined.csv")  # Replace with your CSV path

# Step 3: Encode categorical variables
# Sex, Jaundice, Family_ASD are categorical
le_sex = LabelEncoder()
le_yn = LabelEncoder()
le_class = LabelEncoder()

data['Sex'] = le_sex.fit_transform(data['Sex'])        # m/f -> 0/1
data['Jauundice'] = le_yn.fit_transform(data['Jauundice'])  # yes/no -> 1/0
data['Family_ASD'] = le_yn.fit_transform(data['Family_ASD'])  # yes/no -> 1/0
data['Class'] = le_class.fit_transform(data['Class'])  # NO/YES -> 0/1

# Step 4: Separate features and target
X = data[['A1','A2','A3','A4','A5','A6','A7','A8','A9','A10','Age','Sex','Jauundice','Family_ASD']]
y = data['Class']

# Step 5: Split into train/test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 6: Train the model
model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)

# Step 7: Test the model
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
cr=classification_report(y_test, y_pred)
print(cr)
print("\nClassification Report:\n", )

dump(model, "AutismDecisionTree.joblib")
print("Model saved as AutismDecisionTree.joblib")
import seaborn as sns
import matplotlib.pyplot as plt
op=['Autism','Normal']
import numpy as np
report = classification_report(y_test, y_pred, target_names=op, output_dict=True)
report_df = pd.DataFrame(report).transpose()

# Select only class metrics
metrics = ['precision', 'recall', 'f1-score']
classes = ['Autism','Normal']
data = report_df.loc[classes, metrics]

# Setup positions
x_pos = np.arange(len(classes))
y_pos = np.arange(len(metrics))
xpos, ypos = np.meshgrid(x_pos, y_pos, indexing="ij")
xpos = xpos.flatten()
ypos = ypos.flatten()
zpos = np.zeros_like(xpos)

# Flatten data values
dz = data.to_numpy().flatten()

# Bar dimensions
dx = dy = 0.4

# Assign colors by class
colors = ['#FF9999', '#99CCFF', '#99FF99']  # One color per class
bar_colors = [colors[x] for x in xpos]  # Match color by class index

# Plotting
fig = plt.figure(figsize=(10, 6))
ax = fig.add_subplot(111, projection='3d')

ax.bar3d(xpos, ypos, zpos, dx, dy, dz, shade=True, color=bar_colors, edgecolor='gray')

# Set axis labels
ax.set_xticks(np.arange(len(classes)) + dx / 2)
ax.set_xticklabels(classes)
ax.set_yticks(np.arange(len(metrics)) + dy / 2)
ax.set_yticklabels(metrics)
ax.set_zlabel('Score')

ax.set_title("RF")

plt.show()



# 2. Convert to DataFrame and remove unnecessary rows (like accuracy/support)
df = pd.DataFrame(report).transpose()
# Optional: filter out 'accuracy' and 'support' column if you only want metrics
df_plot = df.drop(columns=['support']).drop(['accuracy'], axis=0)

# 3. Create the 2D heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(df_plot, annot=True, cmap='Blues', fmt=".2f")
plt.title('Classification Report')
plt.show()