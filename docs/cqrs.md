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

## When not to use
- small projects
- MVP
 
## Resources 
- [Основы CQRS](https://habr.com/ru/company/simbirsoft/blog/329970/)
- [Implementing the Clean Architecture](https://cleanarchitecture.io)
- [Command and Query Responsibility Segregation (CQRS) на практике](https://blog.byndyu.ru/2014/07/command-and-query-responsibility.html)
- [Cosmic python](https://www.cosmicpython.com/book/chapter_12_cqrs.html)
