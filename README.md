```mermaid

erDiagram

user ||--|| match_ID:""
match_ID ||--o{ player: ""

user{
    integer user_id
    string password
}

match_ID {
  integer date
  integer score
  string HorA
  string VSteam
}

player {
  string position
  integer number
  integer goal
  integer asist
  integr assessment
}