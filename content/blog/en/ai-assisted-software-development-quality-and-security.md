---
title: "AI assisted software development: how to protect quality and data security"
description: The controls we apply to protect code quality, the confidentiality of corporate data, compliance with data protection law and supply chain security while building faster with AI coding tools.
slug: ai-assisted-software-development-quality-and-security
date: 2026-11-09
author: mert
category: AI and security
order: 3
tr: yapay-zeka-destekli-yazilim-gelistirme-kalite-ve-guvenlik
---

AI assisted coding tools have fundamentally changed how software is built in just a few years. An experienced engineer can now deliver the same work in noticeably less time than before. This speed has made custom software accessible to organizations that previously could not consider it because of budget.

But for corporate clients, speed is not the real question. The real question is: **Is code produced faster just as good and just as secure?** And, even more importantly: **Where does the organization's data go in the process?**

As a team that spent years working on banking systems, we take these questions seriously. In this article we explain how we protect quality and data security in AI assisted development, what commitments we make to our clients, and what questions you should ask a vendor.

## What AI does, and what it does not

First, expectations need to be set correctly. AI coding tools:

- Quickly produce repetitive code, test scaffolding and documentation
- Can read and explain an existing codebase and help with debugging
- Can quickly turn a solution described by an experienced engineer into code

But they **cannot on their own**:

- Know your business rules, exceptions and regulatory requirements
- Decide which solution is right for your organization
- Guarantee that the code they produce is correct; they can produce code that looks convincing but is wrong

That is why AI is not a tool that replaces the engineer but a very powerful tool in the engineer's hands. Responsibility always stays with the team that delivers the code.

## Quality: speed does not mean skipping controls

Code produced with AI must pass every control applied to code written by people. In fact, these controls matter more as speed increases, because more code is produced in less time.

### Human review is mandatory

Every line produced is read, understood and approved by an engineer. "It seems to work" is not an approval criterion. The reviewer must be able to answer: What does this code do, why does it do it this way, and in what situation does it break?

### Tests come with the code

One of the most useful applications of AI is writing tests. Automated tests are written for every business rule and run on every change. Tests are also the most reliable way to document business rules within the team.

There is a trap to watch for here: when the same tool produces both the code and its test at the same time, the test can repeat the code's mistake. That is why, for critical business rules, we first define the test scenarios together with the business side and only then write the code.

### Automated checks catch every change

Every code change passes through an automated pipeline before it is merged:

- **Static analysis.** Scanning for code quality, faulty patterns and known classes of security vulnerabilities
- **Secret scanning.** Preventing passwords, API keys or connection details from accidentally entering the code
- **Dependency scanning.** Checking open source libraries for known security vulnerabilities
- **Licence checks.** Verifying that the licences of added libraries are suitable for commercial use

### Watch out for invented dependencies

AI tools sometimes suggest a library name that does not exist. Malicious actors can register such names in advance and publish harmful code under them. That is why every new dependency added to a project is approved by hand after checking its name, publisher and history.

## Data security: where does client data go?

This is, rightly, the question corporate clients ask most. Our answer is clear, and it is reflected in our contracts.

### Real client data is never given to AI tools

What is shared with AI tools during development is code and technical context, not the client's real data. Employee details, customer records, financial data or contract contents are never given to these tools as input under any circumstances.

In development and test environments, instead of real data:

- **Synthetic data** that mimics the structure of real data is generated
- If real data is unavoidable, copies with personal data **masked or anonymized** are used
- Access to production data is restricted to authorized people and logged

### Tools with enterprise terms are preferred

We choose the AI services we use through enterprise agreements that clearly state that inputs are not used for model training and that set out data retention terms. Free public chat interfaces are not used in corporate projects.

When talking to your vendor, be sure to ask: Does the tool used train its models on our inputs? How long, and in which country, are inputs stored?

### In-house options for sensitive projects

Some organizations require that not even the source code leaves the organization. In that case the options are:

- Using AI tools only with models approved by the organization and running in the organization's own cloud account
- Running open models on the organization's own infrastructure
- Not using AI tools at all in certain parts of the project

This choice is made together at the start of the project and written into the contract. The organization sets the balance between speed and confidentiality; we implement it.

## Data protection law and international transfers

Personal data protection law applies to the use of AI tools as well. In Türkiye this is the Personal Data Protection Law (KVKK). If an AI service runs on servers abroad, sending personal data to it may count as an international transfer of personal data and bring additional obligations.

That is why the basic principle we apply is simple: personal data is not sent to AI tools. This way, the development process itself does not affect the organization's obligations on international transfers.

If the software being built includes an AI feature, for example a module that summarizes documents or classifies requests, that is a separate design matter. Which data goes to which service, where it is processed and how it is logged are decided together with the organization's legal and information security teams.

> This section is general information and does not constitute legal advice. For an assessment of your organization's specific situation, we recommend consulting your legal advisor.

## AI inside the software: new risks

When AI is used not only as a development tool but as part of the product, new kinds of risk appear. The foremost is **prompt injection**: instructions placed inside a document or e-mail that the model processes can try to change the model's behaviour.

Our main safeguards against this risk:

- The data the model can access and the actions it can take are kept to the minimum the task requires
- Model output is validated, or put to human approval, before any critical action
- Content coming from users or external sources is clearly separated from system instructions
- The inputs the model receives and the decisions it makes are logged for audit

## Audit trail and transparency

In regulated industries, how software was built must also be traceable. That is why:

- Every change is kept in version control with who made it and who approved it
- Architectural decisions and their reasoning are documented in writing
- When the project is delivered, the source code, documentation and test infrastructure are handed over to the organization

The client owning the source code is a natural result of this transparency. The organization can have its software audited by an independent team at any time.

## Questions to ask a vendor

Before working with a software team that uses AI assisted development, ask for written answers to these questions:

1. Which AI tools do you use, and under what contract terms?
2. Do these tools use our inputs for model training?
3. Is any of our organization's real data sent to an AI tool during development?
4. What data is used in the test environment? How is personal data masked?
5. What review and testing processes does AI produced code go through?
6. Are dependency, secret and licence scans automated?
7. Will the source code and documentation be handed over to us at the end of the project?
8. Can we restrict the use of AI tools in certain parts of the project if needed?

## Conclusion

> When set up properly, AI assisted development makes custom software faster and more accessible. What protects quality is not the tool but the discipline around it: human review, automated tests and scans.
>
> What protects data security is a clear principle: the organization's real data never enters development tools, the services used are chosen on enterprise terms, and in sensitive projects control stays entirely with the organization.

If you are curious how AI has changed the cost equation of custom software, take a look at our [off-the-shelf or custom software guide](../build-vs-buy-custom-software/).
