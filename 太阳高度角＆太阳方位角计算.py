import ephem
from datetime import datetime, timedelta
import math

def convert_degrees(degrees, minutes, seconds, direction):
    """将度分秒转换为十进制度，并考虑方向（N/S/E/W）"""
    if direction in ['S', 'W']:
        return -(degrees + minutes / 60.0 + seconds / 3600.0)
    else:
        return degrees + minutes / 60.0 + seconds / 3600.0

def validate_coordinates(degrees, minutes, seconds):
    """验证经纬度的有效性"""
    if not (0 <= degrees <= 180 and 0 <= minutes < 60 and 0 <= seconds < 60):
        return False
    return True

def validate_time(time_str):
    """验证时间格式是否正确"""
    try:
        datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        return False

def get_latitude():
    """获取并验证纬度输入"""
    while True:
        try:
            latitude_degrees = float(input("纬度（度）: "))
            latitude_minutes = float(input("纬度（分）: "))
            latitude_seconds = float(input("纬度（秒）: "))
            latitude_direction = input("纬度方向 (N/S): ").upper()

            if not validate_coordinates(latitude_degrees, latitude_minutes, latitude_seconds):
                raise ValueError("纬度值无效，请重新输入！")

            return latitude_degrees, latitude_minutes, latitude_seconds, latitude_direction
        except ValueError as e:
            print(e)

def get_longitude():
    """获取并验证经度输入"""
    while True:
        try:
            longitude_degrees = float(input("经度（度）: "))
            longitude_minutes = float(input("经度（分）: "))
            longitude_seconds = float(input("经度（秒）: "))
            longitude_direction = input("经度方向 (E/W): ").upper()

            if not validate_coordinates(longitude_degrees, longitude_minutes, longitude_seconds):
                raise ValueError("经度值无效，请重新输入！")

            return longitude_degrees, longitude_minutes, longitude_seconds, longitude_direction
        except ValueError as e:
            print(e)

def get_time():
    """获取并验证时间输入"""
    while True:
        try:
            time_input = input("观测时间（格式：YYYY-MM-DD HH:MM:SS）: ")
            if not validate_time(time_input):
                raise ValueError("时间格式不正确，请重新输入！")
            return datetime.strptime(time_input, '%Y-%m-%d %H:%M:%S')
        except ValueError as e:
            print(e)

def calculate_solar_position(latitude, longitude, time_utc):
    """根据经纬度和时间计算太阳的高度角和方位角"""
    # 创建观测者对象
    observer = ephem.Observer()
    observer.lat = str(latitude)
    observer.lon = str(longitude)
    
    # 将北京时间转换为UTC时间
    utc_offset = 8 * 3600  # 北京时间比UTC快8小时
    time_utc = time_utc - timedelta(seconds=utc_offset)

    # 设置观测时间
    observer.date = time_utc.strftime('%Y/%m/%d %H:%M:%S')

    # 计算太阳的位置
    sun = ephem.Sun(observer)
    
    # 返回太阳的高度角和方位角
    return math.degrees(sun.alt), math.degrees(sun.az)

def main():
    print("请输入您的位置信息和观测时间（北京时间）:")

    # 获取纬度信息
    latitude_degrees, latitude_minutes, latitude_seconds, latitude_direction = get_latitude()

    # 获取经度信息
    longitude_degrees, longitude_minutes, longitude_seconds, longitude_direction = get_longitude()

    # 转换经纬度为十进制度，并考虑方向
    latitude = convert_degrees(latitude_degrees, latitude_minutes, latitude_seconds, latitude_direction)
    longitude = convert_degrees(longitude_degrees, longitude_minutes, longitude_seconds, longitude_direction)

    # 主循环：允许用户多次输入时间并计算太阳高度角和方位角
    while True:
        # 获取时间信息
        time_utc = get_time()

        # 计算太阳高度角和方位角
        solar_elevation, solar_azimuth = calculate_solar_position(latitude, longitude, time_utc)
        print(f"太阳的高度角为: {solar_elevation:.2f} 度")
        print(f"太阳的方位角为: {solar_azimuth:.2f} 度")

        # 询问用户是否继续
        continue_input = input("是否继续输入其他时间？(y/n): ")
        if continue_input.lower() != 'y':
            break

if __name__ == "__main__":
    main()