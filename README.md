# TaskFlow - Flask Task Management Application

A professional Flask task management application that uses a JSON file as a database. Features include user management, task assignment, comments, and full CRUD operations. Perfect for deployment on Azure App Service.

## 🚀 Quick Start

**Clone and run in 3 steps:**

```bash
git clone https://github.com/udayrealm/appservicejsonapp.git
cd appservicejsonapp
pip install -r requirements.txt && python app.py
```

Then open `http://localhost:5000` in your browser!

## Features

- ✅ **Task Management** - Create, Read, Update, and Delete tasks
- 👥 **User Management** - Create and manage users
- 📋 **Task Assignment** - Assign tasks to specific users
- 💬 **Comments System** - Add comments to tasks for collaboration
- 📝 **JSON Database** - No external database required, uses JSON file
- 🎨 **Modern UI** - Professional, responsive web interface
- 🔄 **RESTful API** - Complete API for all operations
- 🔍 **Task Filtering** - Filter by All, Pending, or Completed
- 📊 **Statistics Dashboard** - View task statistics in real-time
- 💚 **Health Check** - Built-in health monitoring endpoint

## Project Structure

```
.
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── templates/         # HTML templates
│   └── index.html     # Frontend interface
├── data.json          # JSON database (created automatically)
├── startup.sh         # Startup script for Azure
└── README.md          # This file
```

## Quick Start - Running the App

### For Sharing with Others

**Repository Link:** `https://github.com/udayrealm/appservicejsonapp.git`

### Prerequisites

- Python 3.8 or higher
- pip (usually comes with Python)
- Git (optional, for cloning)

### Quick Setup Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/udayrealm/appservicejsonapp.git
   cd appservicejsonapp
   ```

   Or download as ZIP from GitHub and extract it.

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Open your browser:**
   Navigate to `http://localhost:5000`

That's it! The app will start and you can start managing tasks.

### Detailed Setup (Optional)

If you want to use a virtual environment (recommended):

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

## API Endpoints

### Get all items
```
GET /api/items
```

### Get a specific item
```
GET /api/items/<id>
```

### Create a new item
```
POST /api/items
Content-Type: application/json

{
  "title": "Task title",
  "description": "Task description",
  "completed": false
}
```

### Update an item
```
PUT /api/items/<id>
Content-Type: application/json

{
  "title": "Updated title",
  "description": "Updated description",
  "completed": true
}
```

### Delete an item
```
DELETE /api/items/<id>
```

### Health check
```
GET /health
```

## Azure App Service Deployment

### Option 1: Deploy using Azure CLI

1. **Install Azure CLI** (if not already installed):
   - Download from: https://aka.ms/installazurecliwindows

2. **Login to Azure**:
```bash
az login
```

3. **Create a Resource Group** (if you don't have one):
```bash
az group create --name myResourceGroup --location eastus
```

4. **Create an App Service Plan**:
```bash
az appservice plan create --name myAppServicePlan --resource-group myResourceGroup --sku B1 --is-linux
```

5. **Create the Web App**:
```bash
az webapp create --resource-group myResourceGroup --plan myAppServicePlan --name <your-app-name> --runtime "PYTHON:3.11"
```

6. **Configure the startup command**:
```bash
az webapp config set --resource-group myResourceGroup --name <your-app-name> --startup-file "gunicorn --bind 0.0.0.0:8000 --timeout 600 app:app"
```

7. **Update requirements.txt** to include gunicorn:
   The requirements.txt should include gunicorn for production deployment.

8. **Deploy using Git**:
```bash
az webapp deployment source config-local-git --name <your-app-name> --resource-group myResourceGroup
```

9. **Push to Azure**:
```bash
git remote add azure <deployment-url>
git push azure main
```

### Option 2: Deploy using Azure Portal

1. Go to [Azure Portal](https://portal.azure.com)
2. Click "Create a resource" → "Web App"
3. Fill in the details:
   - **Subscription**: Your subscription
   - **Resource Group**: Create new or use existing
   - **Name**: Your unique app name
   - **Publish**: Code
   - **Runtime stack**: Python 3.11
   - **Operating System**: Linux
   - **Region**: Choose your preferred region
4. Click "Review + create" then "Create"
5. Once created, go to "Deployment Center"
6. Choose your deployment method (GitHub, Azure DevOps, Local Git, etc.)
7. Upload your code files
8. Go to "Configuration" → "General settings"
9. Set the startup command: `gunicorn --bind 0.0.0.0:8000 --timeout 600 app:app`

### Option 3: Deploy using VS Code Azure Extension

1. Install the "Azure App Service" extension in VS Code
2. Sign in to Azure
3. Right-click on your project folder
4. Select "Deploy to Web App"
5. Follow the prompts

## Important Notes for Azure Deployment

1. **Gunicorn**: Make sure `gunicorn` is in your `requirements.txt` for production
2. **Port**: Azure App Service uses port 8000 by default, but the app will use the PORT environment variable
3. **Startup Command**: Set the startup command in Azure App Service configuration
4. **JSON File Persistence**: The `data.json` file will persist in the app's file system, but consider using Azure Storage for production scenarios with multiple instances

## Production Considerations

For production deployments, consider:

- Using Azure Database or Azure Cosmos DB instead of JSON file
- Implementing authentication/authorization
- Adding rate limiting
- Using Azure Application Insights for monitoring
- Setting up CI/CD pipelines
- Using environment variables for configuration
- Implementing proper error handling and logging

## Troubleshooting

### App not starting
- Check the startup command in Azure App Service configuration
- Review logs in Azure Portal → App Service → Log stream
- Ensure `gunicorn` is in `requirements.txt`

### 500 Internal Server Error
- Check application logs
- Verify JSON file permissions
- Ensure all dependencies are installed

### Port issues
- Azure App Service automatically sets the PORT environment variable
- The app uses `os.environ.get('PORT', 5000)` to handle this

## License

This project is open source and available for use.

