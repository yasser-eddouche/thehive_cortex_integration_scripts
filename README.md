# TheHive-Cortex Integration Scripts

A Python toolkit for automating security incident response workflows using TheHive and Cortex platforms. This integration enables automated alert creation, case management, and threat analysis through Cortex analyzers and responders.

## Features

- 🔍 **Automated Alert Creation**: Generate security alerts with observables
- 📋 **Case Management**: Create and manage investigation cases
- 🔗 **Alert-Case Association**: Link alerts to cases for better organization
- 📁 **File Upload**: Upload suspicious files for analysis
- 🔐 **Hash Generation**: Compute SHA-256 hashes for file integrity
- 🧪 **Cortex Integration**: Run analyzers and responders on observables
- 📊 **Analyzer/Responder Discovery**: List available Cortex components
- 🔄 **Job Monitoring**: Track analysis job progress and results

## Prerequisites

- Python 3.7+
- TheHive 5.x instance
- Cortex instance with configured analyzers/responders
- Valid API keys for both platforms

## Installation

1. Clone this repository:

```bash
git clone https://github.com/yourusername/thehive-cortex-integration.git
cd thehive-cortex-integration
```

2. Install required dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your configuration:

```bash
cp .env.example .env
```

## Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# TheHive Configuration
THEHIVE_URL=http://localhost:9000/api
THEHIVE_API_KEY=your_thehive_api_key_here

# Cortex Configuration
CORTEX_URL=http://localhost:9001/api
CORTEX_API_KEY=your_cortex_api_key_here
CORTEX_ID=your_cortex_instance_id

# Analyzer and Responder IDs (optional)
ANALYZER_ID=your_analyzer_id_here
RESPONDER_ID=your_responder_id_here
```

### Finding Analyzer and Responder IDs

Use the included listing script to discover available components:

```bash
# List all available analyzers
python cortex_list.py analyzers

# List responders for a specific artifact
python cortex_list.py responders case_artifact <artifact_id>
```

## Usage

### Basic Security Incident Handling

```python
from thehive_cortex_integration import handle_security_incident

# Process a suspicious file
alert_id, case_id, hash_observable_id = handle_security_incident(
    ioc="suspicious_file.exe",
    description="Suspicious executable detected by security system",
    file_path="/path/to/suspicious_file.exe"
)

if case_id:
    print(f"Security case created: {case_id}")
```

### Command Line Usage

```bash
# Run with default test file
python thehive_cortex_integration.py

# The script will look for 'task.ps1' in the current directory
```

### Discovering Available Components

```bash
# List all analyzers
python cortex_list.py analyzers

# List responders for a case artifact
python cortex_list.py responders case_artifact 12345

# List responders for an observable
python cortex_list.py responders observable 67890
```

## Script Components

### Main Integration Script (`thehive_cortex_integration.py`)

**Core Functions:**

- `handle_security_incident()`: Main workflow orchestrator
- `create_alert()`: Generate security alerts
- `create_case()`: Create investigation cases
- `create_observable()`: Add observables to cases
- `upload_file_to_case()`: Upload files for analysis
- `run_analyzer()`: Execute Cortex analyzers
- `run_responder()`: Trigger Cortex responders
- `wait_for_analyzer()`: Monitor job completion

### Component Discovery Script (`cortex_list.py`)

**Features:**

- List all available Cortex analyzers
- Display supported data types for each analyzer
- Find responders for specific entities
- Group components by Cortex instance

## Workflow Overview

1. **Connection Testing**: Verify connectivity to TheHive and Cortex
2. **Alert Creation**: Generate alert with initial observables
3. **Case Creation**: Create investigation case
4. **Association**: Link alert to case
5. **Observable Creation**: Add hash observables from files
6. **File Upload**: Upload suspicious files as artifacts
7. **Analysis**: Run configured analyzers on observables
8. **Response**: Trigger responders based on analysis results

## API Compatibility

- **TheHive**: Version 5.x
- **Cortex**: Compatible with TheHive 5 integration
- **Python**: 3.7+ required

## Error Handling

The scripts include comprehensive error handling:

- Connection validation
- API response verification
- File operation safety
- Job status monitoring
- Graceful degradation when optional components fail

## Security Considerations

- Store API keys in environment variables, never in code
- Use TLS/SSL for production deployments
- Implement proper access controls for API keys
- Regular key rotation recommended
- Monitor API usage and access logs

## Troubleshooting

### Common Issues

**Connection Errors:**

```bash
# Test connectivity
python -c "from thehive_cortex_integration import test_thehive_connection, test_cortex_connection; print('TheHive:', test_thehive_connection()); print('Cortex:', test_cortex_connection())"
```

**Missing Analyzers/Responders:**

- Verify Cortex instance is properly configured
- Check analyzer/responder installation and enablement
- Ensure proper data type compatibility

**Job Failures:**

- Check Cortex logs for detailed error messages
- Verify analyzer configuration and API quotas
- Ensure proper network connectivity from Cortex to external services

## Examples

### Example 1: Malware Analysis Workflow

```python
# Configure for VirusTotal analysis
import os
os.environ['ANALYZER_ID'] = 'VirusTotal_GetReport_3_1'
os.environ['RESPONDER_ID'] = 'VirusTotalEmailResponder_1_4'

# Process suspicious file
alert_id, case_id, hash_observable_id = handle_security_incident(
    ioc="malware_sample.exe",
    description="Potential malware detected",
    file_path="./samples/malware_sample.exe"
)
```

### Example 2: Network IOC Analysis

```python
# Configure for network analysis
os.environ['ANALYZER_ID'] = 'Shodan_DNSResolve_1_0'

# Process suspicious domain
alert_id, case_id, hash_observable_id = handle_security_incident(
    ioc="suspicious-domain.com",
    description="Suspicious domain in network traffic"
)
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 📖 [TheHive Documentation](https://docs.thehive-project.org/)
- 📖 [Cortex Documentation](https://github.com/TheHive-Project/Cortex)
- 🐛 [Report Issues](https://github.com/yourusername/thehive-cortex-integration/issues)
- 💬 [Discussions](https://github.com/yourusername/thehive-cortex-integration/discussions)

## Changelog

### v1.0.0

- Initial release
- TheHive 5.x compatibility
- Cortex analyzer/responder integration
- Automated workflow orchestration
- Component discovery utilities

---

**Note**: This tool is designed for security professionals and incident responders. Ensure proper authorization before analyzing files or network indicators in your environment.
