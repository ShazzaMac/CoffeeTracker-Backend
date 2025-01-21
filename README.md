# Coffee Tracker Backend

This is my final major project for Queens University Belfast.  Coffee Tracker is a web application that allows users to track their coffee consumption. It includes features for logging daily intake, viewing consumption history, and setting personal goals.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/YourUsername/CoffeeTracker-Backend.git
   ```

2. Navigate to the project directory:
   ```bash
   cd CoffeeTracker-Backend
   ```

3. Create a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   ```

4. Activate the virtual environment:
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

5. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

6. Run the application:
   ```bash
   python manage.py runserver
   ```

Your application should now be running at `http://127.0.0.1:8000/`.

## Usage

To log a new coffee intake, send a `POST` request to:
POST /api/coffee/log

with the following body:
```json
{
  "amount": 250,
  "type": "Espresso",
  "date": "2025-01-21"
}


### 5. **Contributing**
- others can contribute to the project, whether through opening issues, submitting pull requests, or contributing code.

Example:
```markdown
## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to your branch (`git push origin feature-branch`).
6. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Thanks to Django for the web framework.
- Thanks to Python for the great language!
