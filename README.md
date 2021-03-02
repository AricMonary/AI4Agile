<h1 align="center">
  AI4Agile
</h1>

Provides mutation coverage for your Java programs within the Eclipse IDE. Built on [PIT (Pitest)](http://pitest.org) for reliability.

## What is AI4Agile?

> Faults (or mutations) are automatically seeded into your code, then your tests are run. If your tests fail then the mutation is killed, if your tests pass then the mutation lived.
>
> The quality of your tests can be gauged from the percentage of mutations killed.
>
> *Henry Coles, [pitest.org](https://pitest.org)*

## Main Features

- **Epic Decomposition**: decompose an epic, a combination of 
- **Story Optimization**: optimize stories into 
- **Task Generation**: break stories down into simple tasks.
- **Dependency Visualization**: see direct and indirect relationships between issues.


## Usage

Once the plug-in is installed (see [Installation](#Installation) below), you can run Pitest:
- Right-click on a Java project defining unit tests
- `Run As` > `PIT Mutation Test`

Wait a few seconds, two views should open to show the results:
- **PIT Summary**: shows the percentage of mutation coverage
- **PIT Mutations**: shows the detected mutations and their location in code

It is also possible to run a single JUnit test class. Specific PIT options can be configured from the Launch Configuration window:
- `Run` > `Run Configurations...`
- Double-click on `PIT Mutation Test`
- Specify the options
- Press `Run`

Preferences also allow to change mutation settings (`Window > Preferences > Pitest`).

## Installation

The app will soon be available in the [Atlassian Marketplace](https://marketplace.atlassian.com/).