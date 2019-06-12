# EDMC
Enigma Database Managing Class

One simple interface to access and modify many different types of Document based NoSQL Databases. Documentation coming soon.

Interface: v1

### About
NoSQL databases, unlike SQL database, do not have a unified interface to work with. This is a project spun-off from a NoSQL database I wrote in the late 2017. (Or early 2018, idk) Since the NoSQL databases don't have a unified interface, it creates a lock-in with the databases you use, making it hard to migrate databases. This project aims to fix that.

#### Cons
Since the interface for the databases with different features and data structures are equal, some important features can be left out from the interface. That's the case with the current interface, which I call "v1". In later versions, I may come up with a solution.

### Databases supported
 - My custom DB
 - GCP Cloud Firestore

### v1 Interface
Only read/write for Document based NoSQL databases. No query, no delete. Not designed for this project.

### v2 Interface
??? Coming soon.
