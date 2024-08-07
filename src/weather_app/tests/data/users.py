# Users and auth data
empty_credentials = {}
missing_password_credentials = {"email": "invalid@test.com"}
missing_email_credentials = {"password": "456"}
invalid_credentials = {"email": "invalid@test.com", "password": "456"}
admin_credentials = {"email": "admin@weatherapp.com", "password": "123admin"}
admin_uuid = "fc433d73-c3f5-4dfc-a910-9c8111cc20bf"
user_credentials = {"email": "user@test.com", "password": "123user"}
user_uuid = "996b39fc-e09a-4d05-a313-25cf9bc157a5"
station0_user_credentials = {
    "email": "station0@weatherapp.com",
    "password": "123station0",
}
station0_user_uuid = "98313462-8ad1-4d1e-9901-8cdfd64c759f"
station1_user_credentials = {
    "email": "station1@weatherapp.com",
    "password": "123station1",
}
station1_user_uuid = "22f93f9e-f645-44bc-875a-93fa2cf7190f"
test_station_user_credentials = {
    "email": "test_station1@weatherapp.com",
    "password": "123station",
}
test_station_user_uuid = "dd478d01-be0b-421d-bb5e-5b2970c013ba"
expired_refresh_token_admin = "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyMjY5OTc2MSwiaWF0IjoxNzIyNjEzMzYxLCJqdGkiOiJiM2Q3ZDUwZmIxYWI0ZjQ4YmVmMGI4NDhmZjU1ODFlOCIsInVzZXJfdXVpZCI6ImZjNDMzZDczLWMzZjUtNGRmYy1hOTEwLTljODExMWNjMjBiZiIsInVzZXJfaWQiOjEsImlzX3N1cGVydXNlciI6dHJ1ZSwiaXNfc2VydmljZV9zdGF0aW9uIjpmYWxzZX0.s1G_SKkjQW9rz8eZ8LVRPujPaQDWkpGf_HBZXmRPTspT_YKyYIA8DqR3BLeR63mMHap3_H6_8ge_c1ouyipGOEKBb0HsS4XQYOTSO5g6-Wt7Uayawr0a_Xyys8teh05V41DAcYGHQPhGmwesz8ouPTasQnm7D_GPZFrwaTQnh1GCJCsKRBE9UCZbXl1uDzCa0lf0Y1fUa5oSgq1J5vGcVZx3G7_yPVNOFqcGj4Txa1fbM54J9hMnwnC4-qSd2CyOJzhBXdEaT75gyiOJK5fhqITvQ0Q1ci5R2e6iXX35Ly3Z6s-i8iMoslVi4K0st85xbvyqa8kePPR4VAvZ-zFmHg"
expired_refresh_token_user = "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyMjY5OTgyOCwiaWF0IjoxNzIyNjEzNDI4LCJqdGkiOiJkM2Y2NDc1ZThkZDI0ZDczYjkzMTYyNWUyZTQwNmVkNyIsInVzZXJfdXVpZCI6Ijk5NmIzOWZjLWUwOWEtNGQwNS1hMzEzLTI1Y2Y5YmMxNTdhNSIsInVzZXJfaWQiOjEyLCJpc19zdXBlcnVzZXIiOmZhbHNlLCJpc19zZXJ2aWNlX3N0YXRpb24iOmZhbHNlfQ.qraFynAhggMyJh5Hhy8BWPSjHnrCHp0riyR8VON8o6SiuiZyyPDx0PUc8gF_MSzV2Gmr3m-Nh-4MfuSoQo_2qd5zTvEPl3s2iw2Wn7YQ6s_eUKlKWxiE1K3LoheJp4s0ync3317QtnuyYV_jjXgnPQyl8b10zsO5A8Q5PZ6t1dqeJk4xSKEgUcSa4tZ58OTLOV8466QsMGrI91KeFEhyqjwPxMVf3uR7TveaE8jIHQZb0a30baIj_rQCu4mTkWFFotIK1_57IQ5FLNMOO_G4eIj0s8aeFCHhOhkc4vnWfXrBi0HMBbBwAj8o0fldWqaOLXxc426h0A1eo5nflp-nuA"
expired_refresh_token_station = "eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcyMjY5OTg1NywiaWF0IjoxNzIyNjEzNDU3LCJqdGkiOiJkMDAwMTMzYjFlNGY0YWUwODZkZWVlMGJiNTI4NTYzNSIsInVzZXJfdXVpZCI6Ijk4MzEzNDYyLThhZDEtNGQxZS05OTAxLThjZGZkNjRjNzU5ZiIsInVzZXJfaWQiOjIsImlzX3N1cGVydXNlciI6ZmFsc2UsImlzX3NlcnZpY2Vfc3RhdGlvbiI6dHJ1ZX0.mnsEiFgvXNzsK4K_YsCy2o30N7oef1OAokw0I8QH03jrQK3_j1APieaynVBVpLG8OMqz4hzmzaIZMNYU_Y7KEYrrVtpWwz884SVPkd8Hccs9EhVuGlf7_PFj6H_Tmqed5YNS45eLuAmFLbOTdN3QSnNJJpQj42ogL_Z-DenfS0tzjaCi5jt12qlecbOfrJBxCBxjrlUaN8xbI5Ug4RZA-0JeT_cBg5jOwxczKsfBI0Nb0p3FG-skQ_-Mk2sz1NlCc-yFEYvk4TCt9mmlG0d-LNZCZV2_jHkRMZjnqthS_aQsVEt5LqB_sVgGpUHS0TlnNGSkqH4Yq6-7YD-S6LFOQw"

# Registration test data
new_user_empty_data = {}
new_user_missing_email_data = {"password": "456"}
new_user_missing_password_data = {"email": "newuser1@test.com"}
new_user_existing_email_data = {"email": "user@test.com", "password": "456"}
new_user_valid_data = {"email": "newuser@test.com", "password": "456"}

# List/filter user test data
total_users_count = 33
# query_params + count
admin_users_filter = [{"user_type": "admin"}, 1]
station_users_filter = [{"user_type": "service_station"}, 11]
viewer_users_filter = [{"user_type": "viewer"}, 21]

# Update user test data
updated_user_data_valid = {"is_active": False}
updated_user_data_invalid = {"is_active": "test"}
updated_user_data_ignored = {"is_superuser": True}
