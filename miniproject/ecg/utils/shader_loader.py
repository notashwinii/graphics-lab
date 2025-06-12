import OpenGL.GL as gl


def load_shader(shader_path, shader_type):
    """Load and compile a shader from file"""
    with open(shader_path, 'r') as file:
        shader_source = file.read()

    shader = gl.glCreateShader(shader_type)
    gl.glShaderSource(shader, shader_source)
    gl.glCompileShader(shader)

    # Check compilation status
    if not gl.glGetShaderiv(shader, gl.GL_COMPILE_STATUS):
        error = gl.glGetShaderInfoLog(shader).decode()
        raise RuntimeError(f"Shader compilation failed: {error}")

    return shader


def create_shader_program(vertex_path, fragment_path):
    """Create and link a shader program"""
    vertex_shader = load_shader(vertex_path, gl.GL_VERTEX_SHADER)
    fragment_shader = load_shader(fragment_path, gl.GL_FRAGMENT_SHADER)

    program = gl.glCreateProgram()
    gl.glAttachShader(program, vertex_shader)
    gl.glAttachShader(program, fragment_shader)
    gl.glLinkProgram(program)

    # Check linking status
    if not gl.glGetProgramiv(program, gl.GL_LINK_STATUS):
        error = gl.glGetProgramInfoLog(program).decode()
        raise RuntimeError(f"Shader program linking failed: {error}")

    # Clean up individual shaders
    gl.glDeleteShader(vertex_shader)
    gl.glDeleteShader(fragment_shader)

    return program
