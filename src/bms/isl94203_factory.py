from bms.isl94203 import ISL94203


class ISL94203Factory:
    """
    Factory class for ISL94203
    """
    _instance = None

    @classmethod
    def create_instance(cls):
        if not cls._instance:
            cls._instance = ISL94203()
        return cls._instance
