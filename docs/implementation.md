# Implementation 

## Principles

- compromise separation infrastructure from business layers
- communication between layers via simple serializable objects
- all business logic, validation, is contained in the business layer
- API, views, celery tasks prepares raw data for transmission to the business layer
- a unified approach to building the interaction of levels
- wide using interfaces, dependency injection
- keep the usual django folder organization

## Workflow

### API, pages

```mermaid
  sequenceDiagram
    participant Router 
    participant API View 
    Note right of API View: create query/command by <br/>input serializers/forms 
    Router->>API View: request 
    participant CQRS query/command bus 
    API View->>CQRS query/command bus: query/command 
    CQRS query/command bus->>CQRS query/command handler: query/command 
    CQRS query/command handler->>CQRS query/command bus: query/command result
    CQRS query/command bus->>API View: query/command result
    API View->>Router: response 
    Note left of API View: create response by <br/>output serializers/templates
```

## Developing principles

- typing, linters
- tests (pytest)
- single class per file (model per file,...)
- documentation API
- separate view per API method
- reduction of cognitive load by small modules
