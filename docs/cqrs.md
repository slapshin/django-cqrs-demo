# Architecture

## Terminology
- **command** - change the state of an object **_without_** returning a value.
- **query** - returns the result without changing the state of the object. In other words, **_query has no side effects_**
- **command bus** - commands dispatcher
- **query bus** - queries dispatcher

## Advantages
- fewer dependencies in each class
- the principle of sole responsibility (SRP) is respected
- it fits almost everywhere
- easier to replace and test
- functionality expands more easily
- universal workflow between components 

## Limitations
- many small classes appear
- may be difficult to use a group of commands in a single transaction;
- requires developer experience
- 

## When not to use
- small projects
- MVP
