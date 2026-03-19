## Contributing Improvements

If this importer doesn't handle your export correctly:
1. Open an issue with a sample file (anonymized if needed)
2. Describe what went wrong
3. Or fix it yourself and submit a PR — the importer is at `tools/importers/[source_id].py`
```

### Step 6: Register in Registry

Read `registry.json` from the project root and add an entry to the `data_sources` array:

```json
{
  "id": "[source_id]",
  "name": "[Human-readable name]",
  "format": "[File format description]",
  "type": "[quantitative|qualitative|references|mixed]",
  "importer": "tools/importers/[source_id].py",
  "doc": "data_sources/[source_id].md",
  "builtin": false,
  "notes": "[Brief description]"
}
```

Write the updated `registry.json` back.

### Step 7: Create the data_sources Directory (If Needed)

If `data_sources/` doesn't exist at the project root, create it. This is where all data source documentation lives.

### Step 8: Test

If the contributor provided a sample file:
1. Run the importer against it
2. Verify the output files are in the right locations
3. Verify the output format matches theory-forge's expectations
4. Run `/explore-data` to confirm the data is discoverable

If no sample file:
1. Tell the contributor what to test
2. Provide exact commands to run
3. Describe what correct output should look like

### Step 9: Review with Contributor

Show the contributor:

```
Here's what I've created:

1. **Importer**: `tools/importers/[source_id].py`
   - Reads: [format]
   - Writes: [what and where]
   - [Notable design decisions]

2. **Documentation**: `data_sources/[source_id].md`
   - Export instructions for [tool]
   - Import instructions
   - Known limitations

3. **Registry entry** in `registry.json`

To test: [specific test command]

To contribute upstream: Copy these three files into a theory-forge fork and open a PR.

Questions:
- Does the export instruction match how [tool] actually works?
- Are there edge cases in your data I should handle?
- Anything missing from the documentation?
```

---
