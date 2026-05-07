#!/usr/bin/env bash
set -euo pipefail

# Run from project root regardless of where this script is invoked from.
cd "$(dirname "$0")/.."

# Seeds 5 flatmate user profiles + 5 listings (one per major locality, varied
# BHK / furnishing / gender_pref). Profiles are upsert-by-phone so the script
# is rerun-safe for users; listings are created fresh each run (delete the
# previous batch first if you want to avoid duplicates).
#
# Constants (id-based, see app/db/seeds/):
#   localities:   1 DLF Phase 1, 2 Sector 46, 3 Cyber City, 4 Manesar,
#                 5 Golf Course Road, 6 Sushant Lok 1, 7 South City 1
#   bhk:          1 ONE_BHK, 2 TWO_BHK, 3 THREE_BHK, 4 STUDIO
#   gender:       1 Male, 2 Female, 3 Other
#   furnishing:   1 Furnished, 2 Semi, 3 Unfurnished
#   move_in:      1 ASAP, 2 Within 1 month, 3 1-3 months
#   room_type:    1 Single Room, 2 Sharing, 3 Either
#   listing gp:   1 Girls only, 2 Boys only, 3 Mixed

API="${API:-http://localhost:8000}"
ALL_LOCALITIES='[1,2,3,4,5,6,7]'
ALL_BHKS='[1,2,3,4]'
ALL_FURNISHINGS='[1,2,3]'

upsert_user() {
  local body="$1"
  curl -fsS -X POST "${API}/profile" \
    -H 'content-type: application/json' \
    -d "${body}" \
    | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])"
}

create_listing() {
  local body="$1"
  curl -fsS -X POST "${API}/listings" \
    -H 'content-type: application/json' \
    -d "${body}" \
    > /dev/null
}

echo "==> Seeding 5 flatmate profiles"

U1=$(upsert_user "{
  \"phone\": \"7000010001\",
  \"name\": \"Aanya\", \"age\": 26, \"gender\": 2, \"occupation\": 1,
  \"lifestyle_tag_ids\": [1, 5, 8, 17, 20],
  \"preferred_locality_ids\": ${ALL_LOCALITIES},
  \"budget_min\": 15000, \"budget_max\": 30000,
  \"bhk_prefs\": ${ALL_BHKS}, \"room_type_pref\": 1,
  \"furnishing_prefs\": ${ALL_FURNISHINGS},
  \"move_in_pref\": 2, \"gender_pref\": 2
}")
echo "  Aanya  -> id=$U1"

U2=$(upsert_user "{
  \"phone\": \"7000010002\",
  \"name\": \"Rohan\", \"age\": 28, \"gender\": 1, \"occupation\": 2,
  \"lifestyle_tag_ids\": [2, 7, 12, 16, 22],
  \"preferred_locality_ids\": ${ALL_LOCALITIES},
  \"budget_min\": 20000, \"budget_max\": 40000,
  \"bhk_prefs\": ${ALL_BHKS}, \"room_type_pref\": 3,
  \"furnishing_prefs\": ${ALL_FURNISHINGS},
  \"move_in_pref\": 1, \"gender_pref\": 1
}")
echo "  Rohan  -> id=$U2"

U3=$(upsert_user "{
  \"phone\": \"7000010003\",
  \"name\": \"Priya\", \"age\": 24, \"gender\": 2, \"occupation\": 3,
  \"lifestyle_tag_ids\": [3, 4, 13, 23, 21],
  \"preferred_locality_ids\": ${ALL_LOCALITIES},
  \"budget_min\": 12000, \"budget_max\": 25000,
  \"bhk_prefs\": ${ALL_BHKS}, \"room_type_pref\": 2,
  \"furnishing_prefs\": ${ALL_FURNISHINGS},
  \"move_in_pref\": 3, \"gender_pref\": 2
}")
echo "  Priya  -> id=$U3"

U4=$(upsert_user "{
  \"phone\": \"7000010004\",
  \"name\": \"Karan\", \"age\": 30, \"gender\": 1, \"occupation\": 16,
  \"lifestyle_tag_ids\": [10, 11, 18, 20, 16, 24],
  \"preferred_locality_ids\": ${ALL_LOCALITIES},
  \"budget_min\": 25000, \"budget_max\": 50000,
  \"bhk_prefs\": ${ALL_BHKS}, \"room_type_pref\": 1,
  \"furnishing_prefs\": ${ALL_FURNISHINGS},
  \"move_in_pref\": 2, \"gender_pref\": 1
}")
echo "  Karan  -> id=$U4"

U5=$(upsert_user "{
  \"phone\": \"7000010005\",
  \"name\": \"Maya\", \"age\": 27, \"gender\": 3, \"occupation\": 12,
  \"lifestyle_tag_ids\": [3, 6, 13, 14, 19, 21, 24],
  \"preferred_locality_ids\": ${ALL_LOCALITIES},
  \"budget_min\": 18000, \"budget_max\": 35000,
  \"bhk_prefs\": ${ALL_BHKS}, \"room_type_pref\": 3,
  \"furnishing_prefs\": ${ALL_FURNISHINGS},
  \"move_in_pref\": 2, \"gender_pref\": 3
}")
echo "  Maya   -> id=$U5"

echo "==> Seeding 5 listings (varied locality / bhk / furnishing / gender_pref)"

create_listing "{
  \"owner_user_id\": $U1, \"locality_id\": 1, \"monthly_rent\": 22000,
  \"bhk\": 1, \"furnishing\": 1, \"flatmates_needed\": 1, \"gender_pref\": 3,
  \"amenities\": [1, 2, 6, 7], \"move_in\": 2,
  \"photos\": [\"https://ik.imagekit.io/lftm9iczl/listings/dummy1.jpg\"]
}"
echo "  listing 1 (DLF Phase 1, 1BHK, Furnished, Mixed)"

create_listing "{
  \"owner_user_id\": $U2, \"locality_id\": 3, \"monthly_rent\": 35000,
  \"bhk\": 2, \"furnishing\": 2, \"flatmates_needed\": 2, \"gender_pref\": 2,
  \"amenities\": [1, 2, 4, 6, 7, 12], \"move_in\": 1,
  \"photos\": [\"https://ik.imagekit.io/lftm9iczl/listings/dummy2.jpg\"]
}"
echo "  listing 2 (Cyber City, 2BHK, Semi, Boys only)"

create_listing "{
  \"owner_user_id\": $U3, \"locality_id\": 5, \"monthly_rent\": 28000,
  \"bhk\": 3, \"furnishing\": 1, \"flatmates_needed\": 2, \"gender_pref\": 1,
  \"amenities\": [1, 2, 4, 7, 9, 13], \"move_in\": 3,
  \"photos\": [\"https://ik.imagekit.io/lftm9iczl/listings/dummy3.jpg\"]
}"
echo "  listing 3 (Golf Course Road, 3BHK, Furnished, Girls only)"

create_listing "{
  \"owner_user_id\": $U4, \"locality_id\": 4, \"monthly_rent\": 16000,
  \"bhk\": 4, \"furnishing\": 3, \"flatmates_needed\": 1, \"gender_pref\": 3,
  \"amenities\": [1, 6, 13], \"move_in\": 2,
  \"photos\": [\"https://ik.imagekit.io/lftm9iczl/listings/dummy4.jpg\"]
}"
echo "  listing 4 (Manesar, Studio, Unfurnished, Mixed)"

create_listing "{
  \"owner_user_id\": $U5, \"locality_id\": 6, \"monthly_rent\": 30000,
  \"bhk\": 2, \"furnishing\": 2, \"flatmates_needed\": 2, \"gender_pref\": 3,
  \"amenities\": [1, 2, 5, 7, 8, 11], \"move_in\": 2,
  \"photos\": [\"https://ik.imagekit.io/lftm9iczl/listings/dummy5.jpg\"]
}"
echo "  listing 5 (Sushant Lok 1, 2BHK, Semi, Mixed)"

echo "==> Done."
