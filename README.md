# fc_engineer-codetest
This is the source code for the First Circle - Data Engineer code test in line with my Junior Data Engineer role application

*Setup:*
1. Clone this repo and/or open it in codespaces
2. Install the necessary VS Code extensions such as Jupyter Notebook
3. Codespaces is already preinstalled with python so in the terminal just run "python etl_user_transactions.py"
4. For every run, the db will be created (set at 'replace' to prevent incorrect append) with the logs as instructed.
5. To test or query the database, go to file "test_db.ipynb" in the notebooks folder to run some queries

*Summary Report*
From the conducted data exploration here are my findings:

Pricing Table
- 2 seemingly identical products are shown (Samsung TV both priced at 599) with different PUK which may suggest they are different products but with lack of justification would otherwise be treated as the same product

Transactions Table
- transaction fields are incomplete and does not include puk which in the long term would be problematic
- users in the transactions table also has more users than what the users table has
- there are missing and incorrect values in the table (trans_id: 1036, 1044)
