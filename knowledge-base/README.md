# InfraGuid Knowledge Base

This directory contains the local source documents used by the InfraGuid RAG pipeline.

Document groups:

- `company/`: company profile and service catalog
- `security/`: security standards
- `aws/`: AWS VPC, IAM, CloudFront, and Bedrock guides
- `platform/`: Terraform, architecture, platform engineering, and cost standards
- `operations/`: deployment, incident response, incident history, and engagement lifecycle runbooks
- `metadata/`: one JSON metadata file per Markdown document

The backend ingests every Markdown file outside `metadata/`, splits it into overlapping chunks, embeds those chunks with Amazon Titan Text Embeddings V2 through Bedrock, and stores the vectors in ChromaDB.
