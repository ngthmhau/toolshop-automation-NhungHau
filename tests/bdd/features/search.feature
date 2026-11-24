@bdd @ui
Feature: Product search
  As a shopper
  I want to know when my search has no matches
  So that I can try a different search term

  Scenario Outline: A search with no matches shows an empty result
    Given I open the Toolshop home page
    When I search for "<keyword>"
    Then I see the no-results message

    Examples:
      | keyword          |
      | zzznothing999    |
      | no-such-tool-842 |
