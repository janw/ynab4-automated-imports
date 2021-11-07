# YNAB4 Automated Imports

Y4AI – **work-in-progress** of reverse-engineering the YNAB4 file format to enable automated imports of transactions without having to juggle CSV files manually. 🤹

The ultimate goal for this tool is to integrate well with another project of mine, [Cleanab](https://github.com/janw/cleanab), which I currently use to auto-import FinTS/HBCI transactions into my  YNAB Web budget ("nYNAB"). Cleanab is supposed to work with other tools in the future, and YNAB4 shall be one of them.

## Todo

* ~~Create transactions~~ Works with some constraints*
* Add support for working with `.ydiff` files, to avoid loading / maintaining the entire `.yfull` budget.

## *Constraints

* Y4AI currently uses the `.yfull` budget file to modify the budget, and does not consider `.ydiff` files at all. To ensure file consistency, the tool will require you to "Save a Version" in YNAB4 (which updates the yfull file) to work.
* There is no real validation apart from the guessed Pydantic models used to load/save the budget. **Do not use Y4AI with your actual budget without having a backup**.
