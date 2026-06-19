from duplicate_cleanup import deduplicate_existing_records


print()

print("=" * 45)
print("TalentDash Duplicate Cleanup")
print("=" * 45)

duplicates = deduplicate_existing_records()

print()

print(f"Duplicate Records Flagged : {duplicates}")

print()

print("Cleanup Completed.")