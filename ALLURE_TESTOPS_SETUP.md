# Allure TestOps Integration Setup

## Local Setup

### 1. Install Allure Command Line Tool
```bash
# Windows (via scoop)
scoop install allure

# macOS
brew install allure

# Linux
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update
sudo apt-get install allure
```

### 2. Run Tests with Allure
```bash
# Run tests
pytest --alluredir=./allure-results

# View report locally
allure serve ./allure-results

# Or generate static report
allure generate ./allure-results -o ./allure-report --clean
allure open ./allure-report
```

## Docker Setup
```bash
# Run tests in container
docker-compose up tests

# View report with Allure Service
docker-compose up allure
# Open http://localhost:4040 in browser
```

## Allure TestOps Cloud Configuration

### 1. Get Credentials
1. Log into your Allure TestOps instance
2. Go to Profile → API Tokens → Generate new token
3. Note your Project ID from the URL

### 2. Configure GitLab CI Variables
In GitLab: Settings → CI/CD → Variables, add:
- `ALLURE_TOKEN` - Your API token
- `ALLURE_PROJECT_ID` - Project ID
- `ALLURE_TESTOPS_ENDPOINT` - e.g., https://your-company.testops.cloud

### 3. Upload Results Manually
```bash
# Zip results
cd allure-results && zip -r ../allure-results.zip .

# Upload via curl
curl -X POST "${ALLURE_TESTOPS_ENDPOINT}/api/rs/launch/import" \
  -H "Authorization: Api-Token ${ALLURE_TOKEN}" \
  -H "accept: */*" \
  -H "Content-Type: multipart/form-data" \
  -F "launchName=API Tests" \
  -F "projectId=${ALLURE_PROJECT_ID}" \
  -F "results=@allure-results.zip;type=application/zip"
```

## Alternative: Jenkins Integration
```groovy
// In your Jenkinsfile
post {
    always {
        allure [
            includeProperties: false,
            jdk: '',
            properties: [],
            reportBuildPolicy: 'ALWAYS',
            results: [[path: 'allure-results']]
        ]
    }
}
```
