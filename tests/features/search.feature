@bdd @ui
Feature: Product search

  Scenario Outline: A search with no matches shows an empty result
    Given I open the Toolshop home page
    When I search for "<keyword>"
    Then I see the no-results message

    Examples:
      | keyword          |
      | zzznothing999    |
      | no-such-tool-842 |
