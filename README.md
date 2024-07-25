
The goal of this test task is to evaluate two different LLMs with a simple action of “extracting emails signature information and structuring it into a JSON format
## Setup

1. If you don’t have Python installed, [install it from here](https://www.python.org/downloads/).

2. Clone this repository.

3. Navigate into the project directory:

   ```bash
   $ cd ai_tinkerer
   ```

4. Create a new virtual environment:

   ```bash
   $ python -m venv venv
   $ . venv/bin/activate
   ```

5. Install the requirements:

   ```bash
   $ pip install -r requirements.txt
   ```

6. Create an environment variables file:

   ```bash
   $ touch .env
   ```

7. Add your anthropic and openai  api_Keys to the newly created `.env` file.

8. Run the app:

   ```bash
   $ flask run
   ```

You should now be able to access the app at [http://localhost:5000](http://localhost:5000)!
