from bms.isl94203_hal import ISL94203_HAL


class ISL94203Factory:
    """
    Factory class for ISL94203
    """
    _instance = None

    @classmethod
    def create_instance(cls):
        if not cls._instance:
            cls._instance = ISL94203_HAL()
        return cls._instance
