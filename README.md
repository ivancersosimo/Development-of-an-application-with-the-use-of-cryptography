# Development of an application with the use of

# cryptography

## Goal

The goal of this lab is that students learn and know the use of cryptographic libraries to set the
basics of theoretical cryptographic concepts. This assignment describes a general application/
program, whose functionality is up to the students’ choice, though it should carry out a set of
cryptographic operations.

## Description

The program should be developed in Python or Java and it is mandatory the use of the following
cryptographic functions:

- Symmetric and asymmetric encryption
- Hash and HMAC functions
- Digital signatures
- Authentication method

Algorithms should be up to date and not compromised. Then, for instance, AES should be used
for symmetric encryption instead of DES.

**Symmetric and asymmetric encryption and decryption**

At some point in time, the developed program should encrypt and decrypt information and the
result of both operations should be visible. Note that if the encryption process is carried out, for
instance communications, in a transparent way for users, the result could be presented in a log
or in a debug message, as well as the algorithm and the length of the key used.

Concerning key generation:

- Keys should be of appropriate length and in line with the algorithm used.

**Keys generation and storage**

Keys should be protected against possible attacks, though we should consider differences
among symmetric and asymmetric encryption, digital signatures and HMAC:

- Symmetric: encryption and decryption keys are the same. They could be:
    o Stored in a file/ database. As this is a secret key, it could be stored in a protected
       place (for example, encrypted by a password introduced by users)
    o Remembered by users and applied when needed
- Asymmetric: the encryption and decryption keys are different. It is common that given
    their length, users do not introduce the keys, but they are generated, and users apply
    them afterwards because they are:


```
o Stored in a file/ database and the public/ private key is selected accordingly.
Access to the private key could be protected and only accessible using a
password.
```
- Digital signatures: asymmetric encryption is used to generate signatures and then,
    issues to considered are already introduced.
       o Asymmetric keys will be used to generate signatures and they could be also
          applied for asymmetric encryption. However, the use of the PKI described
          afterwards will be used for keys generation.
- HMAC: a single key is used and then, the same issues point out in symmetric encryption
    apply herein.

It should be highlighted the need of generating keys with an appropriate length, as
abovementioned.

**Hashes generation**

Hashes can be used for assorted functions. The following should be considered:

- Their length should be appropriate to prevent attacks. It means that hash algorithms
    cannot be obsolete.
- The computation time could be a relevant requirement is some applications. Then, hash
    functions should be chosen in terms of security and purpose.

**Digital signatures and public key infrastructure**

Each group is a ROOT CERTIFICATION AUTHORITY (AC1). Such authority (AC1) can generate self-
signed certificates or use a PKI as presented in the picture. For administrative issues (for
instance, to have a branch in each community of Spain) there are multiple SUBORDINATE
AUTHORITIES (AC1, AC3...ACN) which can generate public key certificate to users (A, B, C...) as
presented in the image. Then, you must create a PKI composed of a root CA and a subordinate
CA (AC2). Note that you can create this PKI or other one with more levels.

## CA 2 (Subordinate

## authority)

## A

## (person)

## B

## (person)

## CAn (Subordinate

## authority)

## C

## (person)

## CA 1

### (Root certification

### authority)


To limit the amount of work, we assume the existence of a root authority AC1 and a subordinate
authority AC2, which issues certificates to all people who request them or to the
program/application which needs it.

### Authentication methods

Each group may choose the authentication method most appropriate for their program/
application:

- Based on something we know: passwords, though considering robustness and storage
    issues.
- Based on something we have: token, which can be a sms (though not really secure), a
    card, etc. There are multiple alternatives.
- Based on something we are: biometric trait, such as our fingerprint, iris, facial image,
    etc.

### Improvements

There are lots of improvements that can be carried out in terms of cryptography and security.
Some possible improvements are the following:

- Keys stored in a database – it means that keys are properly stored, specially when being
    secret keys.
- Use of different operation modes – using those which are considered secure.
- User input validation – multiple attacks happen due to improper user input validation.
    Thus, validating user input data is a good security practice.
- Other improvements students consider, properly justified.

### Evaluation

Evaluation criteria are defined in the following table.

```
Criterion Maximum score
Development:
Symmetric/ asymmetric encryption 0,
Hash/ HMAC functions 0,
Digital signatures 1,
Authentication 1,
Application complexity and design 0,
Improvements 1 (additional)
Total development 5 (potentially +1)
Reports 2
Defenses 3
Total lab 10
```

### Deliverables

There are 2 reports to deliver. One of them linked to the implementation of symmetric
encryption and hash or HMAC functions, and the other one linked to the implementation of
asymmetric encryption, digital signatures, and improvements, if any.

Each report should answer the following questions and its length should not exceed the one
established. Moreover, **the code should be also delivered properly documented and using
good programming practices**. If these criteria are not followed, there will be penalty in the final
score.

### Delivery 1

**Group:**

**Lab group ID:**

**Name of all students:**

Answer the following questions. Include screenshots to support your arguments.

- What is the goal of the application / program?
- What is symmetric encryption used for? Which are the algorithms that you have used
    and why? How are keys managed?
- What are hash/HMAC functions used for? Which are the algorithms that you have used
    and why? In the case of HMAC, what is/are the key/s managed?

Page limit is 5, excluding cover and annexes. Letter Font should be 11 with simple spacing and
letter type Calibri/ Arial or Times New Roman.

### Delivery 2

**Group:**

**Lab group ID:**

**Name of all students:**

Answer the following questions. Include screenshots to support your arguments.

- What is the goal of the application / program? (Repeat the same as in report 1)
- What is asymmetric encryption used for? Which are the algorithms that you have used
    and why? How are keys managed?
- What are digital signatures used for? Which are the algorithms that you have used and
    why? How are keys managed? Which is the developed PKI?
- What is the implemented authentication? Why have you chosen this type instead of
    other? How have you implemented it?
- If enhancements have been carried out, explain them and given reasons about security
    implications of each of them.

Page limit is 8 , excluding cover and annexes. Letter Font should be 11 with simple spacing and
letter type Calibri/ Arial or Times New Roman.


