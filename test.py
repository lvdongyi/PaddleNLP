# Copyright (c) 2024 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import ast
import os


def extract_all_from_file(file_path):
    """
    使用 ast 模块从文件中提取 __all__ 的值
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            node = ast.parse(file.read(), filename=file_path)

        for elem in node.body:
            # 查找 __all__ 变量
            if isinstance(elem, ast.Assign):
                for target in elem.targets:
                    if isinstance(target, ast.Name) and target.id == "__all__":
                        # 提取 __all__ 的值
                        if isinstance(elem.value, ast.List):
                            return [el.s for el in elem.value.elts if isinstance(el, ast.Str)]
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return None


def find_and_print_all(directory):
    # 遍历指定目录下的所有子目录
    for root, dirs, files in os.walk(directory):
        if "configuration.py" in files:
            # 构造 configuration.py 文件的完整路径
            config_file_path = os.path.join(root, "configuration.py")
            # 提取 __all__ 的值
            all_value = extract_all_from_file(config_file_path)
            if all_value is not None:
                print(f"\nFound __all__ in {config_file_path}:")
                print(all_value)
            else:
                print(f"\n__all__ not found or failed to extract in {config_file_path}")


# 替换为你要检测的目录路径
directory_to_check = "./paddlenlp/transformers"
find_and_print_all(directory_to_check)
