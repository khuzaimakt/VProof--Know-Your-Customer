**VProof-Know Your Customer**

It is a customer verification application. The (model-server) directory contains a algorithm engine backend using FastAPI to perform 3 customer verification modules:

  1. Liveness and anti-spoofing detection on user uploaded image of himself.
  2. Extracting information of the user from his uploaded picture of identity document (ID Card, Passport, Driving License).
  3. Comapriing user uploaded image and image on identity document to verify they are of the same person.
