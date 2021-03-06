AMU-Poznan2014
==============

AMU-Poznan repository for 2014 iGEM

![Sh-miR designer](https://raw.githubusercontent.com/igemsoftware/AMU-Poznan2014/master/images/logoamu.png)

# Sh-miR designer

Sh-miR designer is a project we started during iGEM 2013. This year we would like to continue and expand functionality
of the software. sh-miR designer v1.0 (link) is aimed to create sh-miR molecules based on siRNAs provided by the user.
In sh-miR designer v2.0 only the mRNA number (from NCBI database), which expression should be decreased can be provided.
Moreover, we expanded functionality of the software with off-target validation and check of immune motifs and also
extended miRNA-shuttles database. sh-miR Designer is a software aimed for fast and efficient design of effective RNA
interference (RNAi) reagents - sh-miRs, also known as artificial miRNAs. sh-miRs are RNA particles whose structure is
based on miRNA precursor pri-miRNA, but sequence interacting with transcript is changed depending on research purpose.
Maintenance of structure of pri-miRNA is very important to enable cellular processing and therefore ensure functionality
of artificial particles. sh-miRs delivered to cells on genetic vectors - plasmids or viral vectors - enter natural RNAi
pathway and silence target mRNA. They can be used in genetic therapies and basic biomedical research. We will provide
two applications to access the software, one which require siRNA sequences and the second which require transcript
accession number from NCBI database.

## API

* [README](shmir-api/README.md)
* [Current repository](shmir-api/)
* [Original repository](https://github.com/Nozdi/shmir)

## Website

* [README](shmir-website/README.md)
* [Current repository](shmir-website/)
* [Original repository](https://github.com/gitfred/shmir-website)

## Client

* [README](shmir-client/README.md)
* [Current repository](shmir-client/)
* [Original repository](https://github.com/Nozdi/shmir_client)

Enjoy! :)

# Using this repository

This repository has subtrees of the original repositories. To work with this repo and use subtree stuff, it would be the
best to add following remotes:

```
git remote add shmir git@github.com:Nozdi/shmir.git
git remote add shmir_client git@github.com:Nozdi/shmir_client.git
git remote add shmir_website git@github.com:gitfred/shmir-website.git
```
