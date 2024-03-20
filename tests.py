from uuid_parser import UUIDParser


if __name__ == "__main__":
    uuids_for_tests = (
        "00000000-0000-0000-0000-000000000000", # Nil UUID
        "fb432ea4-e414-11ee-b616-b3ac1c40b0f2", # UUIDv1
        "19c1b668-e415-21ee-d102-1f7dd28d8de4", # UUIDv2 domain=2 (organization), user id=432125544, variant 2 (for tests only)
        "01dd78ef-621d-396f-bd25-db4014f015b4", # UUIDv3 namespace="00000000-0000-0000-0000-000000000000", name="uuid for tests"
        "09076c66-c104-468f-bc96-1425e479eaca", # UUIDv4
        "a711c110-df47-5954-9e7a-c52f8a47bbd1", # UUIDv5 namespace="00000000-0000-0000-0000-000000000000", name="uuid for tests"
        "1eee415a-c0ba-6f04-b251-8d0ab452cbb7", # UUIDv6
        "018e4844-52cc-7277-989a-4a1db39e3b46", # UUIDv7
        "018e4861-5efd-88dc-974a-f4964a2a5bf6", # UUIDv8
        "ffffffff-ffff-ffff-ffff-ffffffffffff", # Max UUID
        "573e0100-1364-ffff-000d-b3e35e8b3c41", # UUIDv1.5
    )

    for num, uuid in enumerate(uuids_for_tests):
        print(f"TEST {num}:")
        print(UUIDParser(uuid))

    print("all tests done.")
