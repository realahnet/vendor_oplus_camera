# proprietary_vendor_oplus_camera

BLOBS BASED ON OnePlus Ace 5 (PKG 110_16.0.5.701)

Prebuilt stock oplus Camera to include in custom ROM builds.

### How to use?

1. Clone this repo to `vendor/oplus/camera`

2. Inherit it from `device.mk` in device tree:

```
# Camera
$(call inherit-product-if-exists, vendor/oplus/camera/opluscamera.mk)
```

3. Inherit it from your `BoardConfig.mk` in device tree:

```
# Camera

-include vendor/oplus/camera/BoardConfigopluscamera.mk
```

4. Ensure that the PRODUCT_BRAND is either oneplus or oppo or realme and that it is not overriden by any of the safetynet hacks.


**NOTE: patches in the patches folder are for YAAP on top of the already picked changes rom has in source. you might need to pick some changes of your own like the vendor tag injection for camera**
**Also needs oplus-fwk changes with proper classes imported**

## Current issues:
- Front lens does not take photos: viewfinder gets stuck
- due to missing oplus gallery, no gallery working when tapped on preview
- portrait mode causes camera hal to get stuck trying to process it so no further photos can be taken. The app crashes eventually
- Random crashes on video recording but it works and saves fine
- HiRes mode is dead
- Slow motion is dead

If you have solutions for any of these with framework patches or whatever please open a PR or something :)

NOTE: SEPOLICY PERMISSIVE IS REQUIRED FOR NOW.
