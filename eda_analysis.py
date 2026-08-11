import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# 1. LOAD DATASET
# ==========================================

df = pd.read_csv("netflix_titles.csv")

print("Original Dataset Shape:", df.shape)


# ==========================================
# 2. HANDLE MISSING VALUES
# ==========================================

# Fill missing text values
df["director"] = df["director"].fillna("Unknown")
df["cast"] = df["cast"].fillna("Unknown")
df["country"] = df["country"].fillna("Unknown")

# Fix incorrect rating values
invalid_ratings = ["74 min", "84 min", "66 min"]

df["rating"] = df["rating"].replace(
    invalid_ratings,
    "Unknown"
)

# Fill missing rating and duration
df["rating"] = df["rating"].fillna("Unknown")
df["duration"] = df["duration"].fillna("Unknown")


# ==========================================
# 3. CONVERT DATE COLUMN
# ==========================================

df["date_added"] = pd.to_datetime(
    df["date_added"],
    errors="coerce"
)


# ==========================================
# 4. CREATE NEW COLUMNS
# ==========================================

df["year_added"] = df["date_added"].dt.year

df["month_added"] = df["date_added"].dt.month_name()


# Extract numerical duration for movies
df["duration_value"] = pd.to_numeric(
    df["duration"].str.extract(r"(\d+)")[0],
    errors="coerce"
)


# ==========================================
# 5. CHECK CLEANED DATA
# ==========================================

print("\n===== CLEANED DATASET SHAPE =====")
print(df.shape)

print("\n===== MISSING VALUES AFTER CLEANING =====")
print(df.isnull().sum())

print("\n===== DUPLICATE ROWS =====")
print(df.duplicated().sum())


# ==========================================
# 6. SAVE CLEANED DATASET
# ==========================================

df.to_csv(
    "cleaned_netflix_titles.csv",
    index=False
)

print("\nCleaned dataset saved successfully!")

# ==========================================
# 7. EXPLORATORY DATA ANALYSIS
# ==========================================

print("\n==========================================")
print("EXPLORATORY DATA ANALYSIS")
print("==========================================")


# ==========================================
# ANALYSIS 1: MOVIES VS TV SHOWS
# ==========================================

type_counts = df["type"].value_counts()

print("\n===== MOVIES VS TV SHOWS =====")
print(type_counts)

plt.figure(figsize=(7, 5))

type_counts.plot(kind="bar")

plt.title("Movies vs TV Shows on Netflix")
plt.xlabel("Content Type")
plt.ylabel("Number of Titles")
plt.xticks(rotation=0)

plt.tight_layout()
plt.savefig("content_type_distribution.png")
plt.show()


# ==========================================
# ANALYSIS 2: CONTENT ADDED BY YEAR
# ==========================================

year_counts = df["year_added"].value_counts().sort_index()

print("\n===== CONTENT ADDED BY YEAR =====")
print(year_counts)

plt.figure(figsize=(10, 5))

year_counts.plot(kind="line", marker="o")

plt.title("Netflix Content Added by Year")
plt.xlabel("Year")
plt.ylabel("Number of Titles")
plt.grid(True)

plt.tight_layout()
plt.savefig("content_by_year.png")
plt.show()


# ==========================================
# ANALYSIS 3: TOP 10 COUNTRIES
# ==========================================

country_counts = (
    df[df["country"] != "Unknown"]["country"]
    .str.split(", ")
    .explode()
    .value_counts()
    .head(10)
)

print("\n===== TOP 10 COUNTRIES =====")
print(country_counts)

plt.figure(figsize=(9, 6))

country_counts.sort_values().plot(kind="barh")

plt.title("Top 10 Countries by Netflix Content")
plt.xlabel("Number of Titles")
plt.ylabel("Country")

plt.tight_layout()
plt.savefig("top_countries.png")
plt.show()


# ==========================================
# ANALYSIS 4: TOP 10 GENRES
# ==========================================

genre_counts = (
    df["listed_in"]
    .str.split(", ")
    .explode()
    .value_counts()
    .head(10)
)

print("\n===== TOP 10 GENRES =====")
print(genre_counts)

plt.figure(figsize=(9, 6))

genre_counts.sort_values().plot(kind="barh")

plt.title("Top 10 Genres on Netflix")
plt.xlabel("Number of Titles")
plt.ylabel("Genre")

plt.tight_layout()
plt.savefig("top_genres.png")
plt.show()


# ==========================================
# ANALYSIS 5: CONTENT RATINGS
# ==========================================

rating_counts = df["rating"].value_counts()

print("\n===== CONTENT RATINGS =====")
print(rating_counts)

plt.figure(figsize=(9, 5))

rating_counts.plot(kind="bar")

plt.title("Netflix Content by Rating")
plt.xlabel("Rating")
plt.ylabel("Number of Titles")
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig("ratings_distribution.png")
plt.show()


# ==========================================
# BASIC STATISTICAL INSIGHTS
# ==========================================

print("\n==========================================")
print("KEY STATISTICAL INSIGHTS")
print("==========================================")

print(
    "\nMost common content type:",
    type_counts.index[0],
    "-",
    type_counts.iloc[0],
    "titles"
)

print(
    "\nMost common genre:",
    genre_counts.index[0],
    "-",
    genre_counts.iloc[0],
    "titles"
)

print(
    "\nMost common rating:",
    rating_counts.index[0],
    "-",
    rating_counts.iloc[0],
    "titles"
)

print(
    "\nTop country:",
    country_counts.index[0],
    "-",
    country_counts.iloc[0],
    "titles"
)

print("\n===== NUMERICAL CORRELATION =====")

correlation = df[
    ["release_year", "year_added"]
].corr()

print(correlation)

print("\nEDA completed successfully!")

# ==========================================
# 8. CORRELATION HEATMAP
# ==========================================

correlation = df[
    ["release_year", "year_added"]
].corr()

plt.figure(figsize=(6, 5))

plt.imshow(correlation, cmap="coolwarm")

plt.colorbar(label="Correlation")

plt.xticks(
    range(len(correlation.columns)),
    correlation.columns,
    rotation=45
)

plt.yticks(
    range(len(correlation.columns)),
    correlation.columns
)

for i in range(len(correlation.columns)):
    for j in range(len(correlation.columns)):
        plt.text(
            j,
            i,
            f"{correlation.iloc[i, j]:.2f}",
            ha="center",
            va="center"
        )

plt.title("Correlation Between Release Year and Year Added")
plt.tight_layout()

plt.savefig("correlation_heatmap.png")
plt.show()