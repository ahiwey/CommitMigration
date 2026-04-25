# Android Follow-up Checklist

Before claiming the migration is complete, quickly inspect whether the migrated change also affects:

- `AndroidManifest.xml`
- custom View fully qualified names in layout XML
- `navigation` XML destinations and arguments
- `provider` declarations
- `authority` strings
- imports and fully qualified class names
- resource names and values-based resources
- reflection strings
- route paths or keys
- serialization model names
- Proguard or R8 rules

## Practical rule

If the source change touched any Android-facing component, search for the component's name and related resource identifiers instead of assuming the code file was the only place that changed.
