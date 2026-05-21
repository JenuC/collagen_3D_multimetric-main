import os
import tifffile


input_dir = r"G:\FluorescentCollagen\20260519_flucol_kpc_ows3\selectedpos\maskapplied_timeseries_stacks"
output_dir = r"G:\FluorescentCollagen\20260519_flucol_kpc_ows3\selectedpos\maskapplied_timeseries_individualslices"

os.makedirs(output_dir, exist_ok=True)


for fname in os.listdir(input_dir):

    if not fname.endswith(".tif"):
        continue

    fpath = os.path.join(input_dir, fname)

    # Read stack
    stack = tifffile.imread(fpath)

    # Remove prefix if desired
    base = os.path.basename(fname)

    print(f"{fname}: shape={stack.shape}")

    # Iterate through z slices
    for s in range(stack.shape[0]):

        slice_img = stack[s]

        out_name = f"{base[:-4]}_s{s+1}.tif"

        out_path = os.path.join(output_dir, out_name)

        tifffile.imwrite(out_path, slice_img)

        print("  saved:", out_name)