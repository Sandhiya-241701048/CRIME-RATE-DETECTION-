# Crime Rate Detection System 🔍

A cloud-based web application built on Microsoft Azure to analyze and visualize crime data.

---

## 👥 Team Members & Modules

| Member            | Module                          | Files                          |
|-------------------|---------------------------------|--------------------------------|
| Vaishnav Perumal  | Authentication                  | `routes/auth.py`               |
| Sandhiya E        | Dataset Management              | `routes/dataset.py`            |
| Meenashi S        | Crime Analysis & Filters        | `routes/analysis.py`           |
| Mukesh V A        | Alerts & Risk Prediction        | `routes/alerts.py`, `ml-model/`|
| Gokul Krishna I S | Dashboard & Reports             | `routes/reports.py`, `frontend/pages/` |

---

## 🛠️ Tech Stack

| Layer      | Technology                        |
|------------|-----------------------------------|
| Frontend   | HTML5, CSS3, JavaScript           |
| Backend    | Python 3.11 + Flask               |
| Database   | Azure SQL Database (in-memory for dev) |
| Storage    | Azure Blob Storage                |
| ML Model   | Python (rule-based, upgradable to scikit-learn) |
| Hosting    | Azure App Service                 |
| Auth       | Session-based (upgradable to Azure AD B2C) |
| DevOps     | GitHub + Azure DevOps             |

---

## 📁 Project Structure

```
crime-rate-detection/
├── backend/
│   ├── app.py                  ← Flask entry point (run this)
│   ├── requirements.txt        ← Python packages
│   ├── routes/
│   │   ├── auth.py             ← Vaishnav: login, logout, validate
│   │   ├── dataset.py          ← Sandhiya: upload, validate, list, delete
│   │   ├── analysis.py         ← Meenashi: summary, filter, trends
│   │   ├── alerts.py           ← Mukesh: safety score, peak time, alerts
│   │   └── reports.py          ← Gokul: generate, list, download reports
│   └── models/
│       └── db.py               ← Data store (in-memory, replace with Azure SQL)
├── frontend/
│   ├── index.html              ← Login page
│   ├── css/style.css           ← All styles
│   ├── js/common.js            ← Shared sidebar + helpers
│   └── pages/
│       ├── user-dashboard.html ← Main dashboard with charts
│       ├── admin-dashboard.html← Admin overview + alerts
│       ├── dataset.html        ← Upload & manage datasets
│       ├── filter-location.html← Filter crimes by city
│       ├── filter-type.html    ← Filter crimes by type
│       ├── trends.html         ← Monthly & hourly trends
│       ├── alerts.html         ← Safety scores & alerts
│       └── reports.html        ← Generate & download reports
├── ml-model/
│   └── crime_predictor.py      ← Mukesh's prediction engine
├── database/
│   └── schema.sql              ← Azure SQL table creation script
└── README.md
```

---

## 🚀 Getting Started

### Step 1: Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/crime-rate-detection.git
cd crime-rate-detection
```

### Step 2: Install Python packages
```bash
cd backend
pip install -r requirements.txt
```

### Step 3: Run the backend
```bash
python app.py
```
✅ Backend runs at: **http://localhost:5000**

### Step 4: Open the frontend
Open `frontend/index.html` in your browser.

### Step 5: Login
| Role  | Email               | Password |
|-------|---------------------|----------|
| Admin | admin@crime.com     | admin123 |
| User  | user@crime.com      | user123  |

---

## 🌐 API Endpoints

### Auth (Vaishnav)
| Method | Endpoint              | Description        |
|--------|-----------------------|--------------------|
| POST   | `/api/auth/login`     | Login              |
| POST   | `/api/auth/logout`    | Logout             |
| GET    | `/api/auth/validate`  | Check session      |

### Dataset (Sandhiya)
| Method | Endpoint                        | Description          |
|--------|---------------------------------|----------------------|
| POST   | `/api/dataset/upload`           | Upload CSV file      |
| POST   | `/api/dataset/validate`         | Validate file        |
| GET    | `/api/dataset/list`             | List all datasets    |
| PUT    | `/api/dataset/update/<id>`      | Update dataset       |
| DELETE | `/api/dataset/delete/<id>`      | Delete dataset       |

### Analysis (Meenashi)
| Method | Endpoint                          | Description           |
|--------|-----------------------------------|-----------------------|
| GET    | `/api/analysis/summary`           | Overall summary       |
| GET    | `/api/analysis/filter/location`   | Filter by location    |
| GET    | `/api/analysis/filter/type`       | Filter by crime type  |
| GET    | `/api/analysis/trends`            | Monthly trends        |
| GET    | `/api/analysis/by-hour`           | Hourly breakdown      |
| GET    | `/api/analysis/top-locations`     | Top crime locations   |
| GET    | `/api/analysis/records`           | All records           |

### Alerts (Mukesh)
| Method | Endpoint                    | Description              |
|--------|-----------------------------|--------------------------|
| GET    | `/api/alerts/safety-score`  | Safety score for location|
| GET    | `/api/alerts/all-scores`    | All location scores      |
| GET    | `/api/alerts/peak-time`     | Peak crime time          |
| POST   | `/api/alerts/check`         | Check alert for location |
| GET    | `/api/alerts/auto`          | All active alerts        |

### Reports (Gokul)
| Method | Endpoint                      | Description            |
|--------|-------------------------------|------------------------|
| POST   | `/api/reports/generate`       | Generate report        |
| GET    | `/api/reports/list`           | List all reports       |
| GET    | `/api/reports/<id>`           | Get specific report    |
| GET    | `/api/reports/dashboard-stats`| Stats for dashboard    |

---

## 🌿 Git Branch Strategy

```
main         ← stable, production code only
dev          ← integration (everyone merges here first)
├── feature/auth        ← Vaishnav
├── feature/dataset     ← Sandhiya
├── feature/analysis    ← Meenashi
├── feature/alerts      ← Mukesh
└── feature/dashboard   ← Gokul
```

**Rule:** Never push directly to `main`. Always create a Pull Request into `dev` first.

---

## ☁️ Azure Services Used

| Service              | Purpose                        |
|----------------------|--------------------------------|
| Azure App Service    | Host the Flask backend         |
| Azure SQL Database   | Store crime records            |
| Azure Blob Storage   | Store uploaded CSV files       |
| Azure AD B2C         | Production authentication      |
| Azure DevOps         | CI/CD pipeline & work items    |
| Azure Machine Learning | Upgrade ML model (future)   |
