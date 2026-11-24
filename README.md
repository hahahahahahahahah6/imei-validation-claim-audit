# Device identifier claim audit

This offline static audit compares documentation claims about device identifier checks with Python source call shapes. It does not execute the inspected code. It uses only the standard library and requires Python 3.9 or newer.

```text
imei-validation-claim-audit
```

Install a local distribution with `python3 -m pip install --no-cache-dir PATH`, then run:

```sh
imei-validation-claim-audit audit .
python3 -m imei_validation_claim_audit audit . --json
imei-validation-claim-audit audit . --ignore vendor --fail-on medium --verbose
```

The optional repository argument defaults to the current directory. Repeated `--ignore PREFIX` options exclude relative path prefixes. The default threshold is `high`; `medium` also fails for test-only evidence. Exit status 0 means the threshold was not reached, 2 means it was reached, and 1 means usage or I/O error. `--version` prints the version.

A positive claim without production evidence yields the following finding, at medium severity if only tests contain evidence and high otherwise:

```text
documented-imei-validation-claim-false
```

A denial contradicted by production evidence yields the following high severity finding:

```text
documented-no-imei-validation-claim-false
```

The audit reads the root README and Markdown files under a `docs` component. It ignores fenced blocks but includes inline code. It normalizes case, contractions, hyphens and whitespace, matches exact phrases within paragraphs, and removes denial spans before matching positive claims. It parses Python files without executing them, excludes symlinks and ignores source under fixtures, docs and examples. Test files count separately. Imports, aliases, local definitions and selected bindings are considered within each module.

The recognized library routes call `validate`, `is_valid`, or `imei_type` from `stdnum.imei`. Device-specific generic function names are recognized as attribute calls or resolved from-import calls. Calls must be present in a single module; syntax errors supply no evidence.

## Differentiation

The following neighbouring capabilities are outside this audit. Each one is a different capability from judging whether a device identifier string is well formed.

Generic input validation checks whether input is checked at all.

Isbn validation checks the isbn 10 or isbn 13 check digit of a book number.

Issn validation checks the check digit of a serial number.

Iban validation checks the check digit of a bank account number.

Uuid validation checks the shape of a universally unique identifier.

Semver validation checks the shape of a semantic version.

Mac address validation checks a hardware address.

Bic validation checks a bank identifier code.

Cron expression validation checks a schedule string.

Cron expression description turns a schedule string into a human readable sentence.

Scheduled execution runs a job on a schedule.

Date validation checks whether a date is a real calendar date.

Timeouts limit how long a call may run.

Payment processing takes a payment from a card.

Credit card extraction reads card details from a document.

Authentication can prove account ownership with a one time code or confirmation link.

Password authentication verifies a password against a stored hash.

Password hashing prepares a password for storage.

Password generation mints a random password.

Pdf encryption protects a pdf with a password.

Email sending delivers mail.

Sms sending delivers a text message.

Document extraction reads data out of a document.

Barcode scanning decodes a code from an image.

Email validation judges an email address or its deliverability.

Phone number validation judges a number or its validity for a region.

Password strength evaluates how strong a password is.

Json schema validation checks json data against a schema.

Credit card validation judges a card number, its luhn check, and recognized brand.

Domain validation checks a bare host name.

Url validation checks a web address.

Ip address validation checks a numeric address.

Json decoding turns text into a value.

Regex matching compares text with a pattern.

Url parsing splits a web address into parts.

Network fetching retrieves a web address.

Dns resolution looks up a name.

Barcode generation encodes an account number in a strip.

Account number extraction reads a number from a document.

Vehicle number extraction reads a number from a registration or image.

Vehicle number decoding splits its sections or looks up make, model, and year.

Vehicle history lookup asks a service about a number.

Hex color validation judges a hexadecimal color string.

Orcid validation judges a researcher identifier.

Isni validation judges a 16 digit identifier.

Doi validation judges whether a digital object identifier names a work.

Doi resolution asks whether a work identifier resolves.

Cusip validation judges a 9 character national identifier on its own.

Sedol validation judges a 7 character london identifier.

Isin validation judges a 12 character securities identifier with a letter expanded luhn check.

Record lookup fetches a security record from a market data service.

Securities identifier extraction reads an identifier from a document.

Meid validation judges a 14 digit hexadecimal mobile identifier.

Serial number validation judges any serial number in general, with no check digit leg.

Device lookup fetches a device record from a registry or carrier service.

Device identifier extraction reads an identifier from a document or a photo.

Spreadsheet reading is a separate claim family.

Spreadsheet generation is a separate claim family.

Word document reading is a separate claim family.

Word document generation is a separate claim family.

Presentation reading is a separate claim family.

Presentation generation is a separate claim family.

Pdf extraction is a separate claim family.

Pdf generation is a separate claim family.

Pdf merging is a separate claim family.

Pdf splitting is a separate claim family.

Pdf rotation is a separate claim family.

Pdf form filling is a separate claim family.

Pdf watermarking is a separate claim family.

Pdf redaction is a separate claim family.

Pdf compression is a separate claim family.

Pdf annotation is a separate claim family.

Table extraction is a separate claim family.

Ocr is a separate claim family.

Document extraction is a separate claim family.

E signature is a separate claim family.

Screen recording is a separate claim family.

Video generation is a separate claim family.

Qr code generation is a separate claim family.

Barcode generation is a separate claim family.

Barcode scanning is a separate claim family.

Audio mixing is a separate claim family.

Audio generation is a separate claim family.

Audio editing is a separate claim family.

Source separation is a separate claim family.

Speech recognition is a separate claim family.

Text to speech is a separate claim family.

Noise suppression is a separate claim family.

Music generation is a separate claim family.

Music transcription is a separate claim family.

## Limitations

Bare imports are not evidence, even when the import is the only thing the module does.

A `.validate` call on a base that is not a `stdnum.imei` base is missed.

A route call must sit in a single module.

A route call on a name the module locally defines is shadowed.

A generic name called through an alias chain the tracer cannot follow is missed.

Dead code counts, because the audit reads code, not execution.

A subprocess call that shells out to an external checker is not evidence by design.

Syntax invalid files give no evidence.

The audit matches exact phrases only, not meaning.

A doc that claims the checked capability in a roadmap, changelog, or todo is still a claim.

A doc that denies the checked capability with a phrase outside the denial list is not recognised as a denial.

A claim in a file that is not the root readme or under a docs path is not read at all.

A validation implementation in another language in the same repo is invisible.

A validation route that only exists at runtime, such as a dynamically imported module or a plugin loaded by name, is invisible.

This is static pattern matching, not a semantic judgement.

`compact` only reformats and is not evidence.

`format` only reformats and is not evidence.

`split` only separates components and is not evidence.

A `meid` call judges a meid, never an imei, and is not evidence.

An `esn` call judges an esn, never an imei, and is not evidence.

An imei lookup call is a lookup and is not evidence.

A length check alone is not evidence.

A tac membership check alone is not evidence.

A bare luhn checksum call with no imei leg is not evidence.

A regex match alone is not evidence.

Naming only the identifier does not constitute a claim.

A generic identifier check alone is insufficient.

A reference to a check digit alone is insufficient.

A reference to luhn alone is insufficient.

A reference to tac alone is insufficient.

A reference to serial number alone is insufficient.

A locally defined generic name is shadowed even when its implementation performs the check.

A result produced by an external platform is still flagged.

A 14 digit input is accepted by the library with no check digit at all.

An `imei_type` call used only to display a type label is a false positive.

A single email check with no imei leg is not evidence.

A single phone number check with no imei leg is not evidence.

A single url check with no imei leg is not evidence.

A single ip address check with no imei leg is not evidence.

A single domain check with no imei leg is not evidence.

A single isbn check with no imei leg is not evidence.

A single issn check with no imei leg is not evidence.

A single iban check with no imei leg is not evidence.

A single isin check with no imei leg is not evidence.

A single meid check with no imei leg is not evidence.

```text
validate imei
```
The bare phrase above can refer to a manual runbook step, yielding a false positive.

```text
imei validation
```
The bare phrase above can refer to a roadmap feature, yielding a false positive.

```text
imei validation
```
The bare phrase above can refer to an external service result, yielding a false positive.

```text
imei validator
```
The bare phrase above can refer to a hosted web page rather than local code, yielding a false positive.

```text
imei check
```
The bare phrase above can refer to a submission rule that only requires a field, yielding a false positive.

```text
check imei
```
The bare phrase above can refer to a manual runbook step, yielding a false positive.

```text
verify imei
```
The bare phrase above can refer to visually identifying the right handset, yielding a false positive.

```text
imei code validation
```
The bare phrase above can refer to checking that a field is filled, yielding a false positive.

```text
valid imei
```
The bare phrase above can appear in example input instructions without an implemented check, yielding a false positive.

```text
imei is valid
```
The bare phrase above can be example output without an implemented check, yielding a false positive.

```text
imei is invalid
```
The bare phrase above can be example error text without an implemented check, yielding a false positive.

```text
imei validity
```
The bare phrase above can name a configuration flag or column, yielding a false positive.

```text
imei format validation
```
The bare phrase above can describe a format without implementation, yielding a false positive.

```text
validate imei number
```
The bare phrase above can refer to shape alone without a TAC check, yielding a false positive.

```text
imei number validation
```
The bare phrase above can name a specification section without implementation, yielding a false positive.

```text
validate imei code
```
The bare phrase above can refer to a manual runbook step, yielding a false positive.

```text
check imei code
```
The bare phrase above can refer to a manual runbook step, yielding a false positive.

```text
validate imeisv
```
The bare phrase above can refer to a manual runbook step, yielding a false positive.

```text
imeisv validation
```
The bare phrase above can name a specification section without implementation, yielding a false positive.

```text
imei number check
```
The bare phrase above can name a checklist item without implementation, yielding a false positive.

```text
imei
```
The bare phrase above names an identifier without asserting a judgment, so it is excluded.

```text
imei number
```
The bare phrase above names an identifier without asserting a judgment, so it is excluded.

```text
validate identifier
```
The bare phrase above can refer to any identifier, so it is excluded.

```text
check digit
```
The bare phrase above names a component without asserting a judgment, so it is excluded.

```text
luhn
```
The bare phrase above names an algorithm shared with card numbers, so it is excluded.

```text
tac
```
The bare phrase above names a code without asserting a judgment, so it is excluded.

```text
serial number
```
The bare phrase above names a broader category without asserting a judgment, so it is excluded.

Human review is needed for every finding.
