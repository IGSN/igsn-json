# IGSN JSON development for the IGSN 2040 Sprint 1 (May/June 2020)
The current implementation of IGSN is an excellent combination of lean centralised functions that are supported by federated services. This has given IGSN the ability to adapt to requirements arising from new communities joining the system. To accommodate a more diverse community of users and a much larger number of sample registrations requires a number of changes.

In particular, there are two new roles within the IGSN architecture – that of an allocating agent, who publishes data in a minimal and cost-effective way, and the data aggregators who provide services that consume and republish that data in more powerful ways (but which potentially come with higher support and service costs). Both of these roles are currently carried out by allocating agents, but by forcing agents to also provide aggregated data services raises the resources required to become an agent and makes the role less sustainable in the longer term.

Under the new scheme, we propose that agents simply publish JSON documents on their landing pages which aggregators can crawl to uncover new data, along with a sitemap pointing to all the landing pages which contain sample data. Agents would not be responsible for providing high-frequency or high-volume query support against this data – that would be the role of the aggregator. Aggregators would have a responsibility to their end-users to provide services that are performant and scientifically useful, removing this burden from the agents.
For the relationship between agents and aggregators to work effectively, we need to outline the contract governing the relationship. In the long run, we want these roles to be as decoupled as possible, but while we are developing recommendations it would be good to have both in the room to ensure that we are balancing the needs of the two roles effectively.

In this sprint we want to test and evaluate the implementation of sharing and aggregating IGSN metadata between IGSN Agents and Metadata Aggregators.

# Aims of testing
* Determine how difficult (or not) it will be for agents to make the required changes to their landing pages to conform to the new requirements and provide crawler guidance in robot.txt and sitemap.xml files.
* Determine how difficult or not it is will be to develop new web crawlers for aggregators to aggregate data
* Uncover any new ways of using aggregated data that might be of interest to the community
* Determine what services IGSN eV needs to provide to agents to support their publication role (e.g. publication of JSON Schema, JSON LD contexts etc, authentication, role-based access etc)
