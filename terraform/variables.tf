variable "lambda_function_name" {
  description = "Name of the Lambda function"
  type        = string
  default     = "jscom-notion-qr-service"
}

variable "s3_bucket" {
  description = "S3 bucket for storing QR code files"
  type        = string
  default     = "media.johnsosoka.com"
}

variable "runtime" {
  description = "Runtime for the Lambda function"
  type        = string
  default     = "python3.9"
}

variable "memory_size" {
  description = "Lambda memory size in MB"
  type        = number
  default     = 128
}

variable "timeout" {
  description = "Lambda timeout in seconds"
  type        = number
  default     = 30
}