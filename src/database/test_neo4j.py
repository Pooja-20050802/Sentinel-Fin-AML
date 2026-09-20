from neo4j_database import get_driver


driver = get_driver()


with driver.session() as session:

    result = session.run("RETURN 'Neo4j Connected!' AS message")

    record = result.single()

    print(record["message"])


driver.close()