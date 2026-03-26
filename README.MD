# PTZ Camera Test

## Dependencies

- `qt6-base`
- `qt6-wayland`
- `mesa`
- `ttf-dejavu`

**Note:**  
If you encounter Qt errors under Wayland (`qt.qpa.plugin`), set the platform explicitly before running the script:

```bash
export QT_QPA_PLATFORM=xcb


## terminal testing setup instructions:

cd path/to/ptz_test
python -m venv venv
source ~/ptz_test/venv/bin/activate
pip install v4l2py linuxpy opencv-python numpy
python ~/ptz_test/test_ptz.py

## controls

- left and right arrow keys pan camera left and right
- up and down arrow keys handle zooming in and out
- q to quit
