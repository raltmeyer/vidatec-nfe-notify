variable "mikrotik_host" {
    type = string
}

variable "mikrotik_username" {
    type = string
    sensitive = true
}

variable "mikrotik_password" {
    type = string
    sensitive = true
}