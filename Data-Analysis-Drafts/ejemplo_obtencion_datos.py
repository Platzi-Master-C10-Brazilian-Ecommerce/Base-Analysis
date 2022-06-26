with engine.connect() as con:
    rs = con.execute("""SELECT * FROM pg_catalog.pg_tables 
                      WHERE schemaname != 'pg_catalog' 
                      AND schemaname != 'information_schema'""")
    row = rs.fetchall()
    df_tables = pd.DataFrame(row)