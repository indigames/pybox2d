from math import sqrt
import sys
import random
import math

from .framework import (Framework, Keys, main)
from Box2D import (b2CircleShape, b2FixtureDef, b2PolygonShape, b2Random, b2EdgeShape, b2MassData,
                   b2Vec2, b2_epsilon, b2BodyDef, b2ChainShape, b2ParticleGroupDef)
from Box2D import (b2ParticleDef, b2ParticleSystem,
                   b2ParticleSystemDef, b2ParticleColor)
import Box2D


class RadialEmitter:
    def __init__(self):
        self.m_particleSystem = None
        self.m_callback = None
        self.m_speed = 0.0
        self.m_emitRate = 1.0
        self.m_emitRemainder = 0.0
        self.m_flags = Box2D.b2_waterParticle
        self.m_group = None

    def SetPosition(self, origin):
        self.m_origin = origin

    def GetPosition(self):
        return self.m_origin

    def SetSize(self, size):
        self.m_halfSize = size * 0.5

    def GetSize(self):
        return self.m_halfSize * 2.0

    def SetVelocity(self, velocity):
        self.m_startingVelocity = velocity

    def GetVelocity(self):
        return self.m_startingVelocity

    def SetSpeed(self, speed):
        self.m_speed = speed

    def GetSpeed(self):
        return self.m_speed

    def SetParticleFlags(self, flags):
        self.m_flags = flags

    def GetParticleFlags(self):
        return self.m_flags

    def SetColor(self, color):
        self.m_color = color

    def GetColor(self):
        return self.m_color

    def SetEmitRate(self, emitRate):
        self.m_emitRate = emitRate

    def GetEmitRate(self):
        return self.m_emitRate

    def SetParticleSystem(self, particleSystem):
        self.m_particleSystem = particleSystem

    def GetParticleSystem(self):
        return self.m_particleSystem

    def SetCallback(self, callback):
        self.m_callback = callback

    def GetCallback(self):
        return self.m_callback

    def SetGroup(self, group):
        self.m_group.SetGroupFlags(
            m_group.GetGroupFlags() & ~Box2D.b2_particleGroupCanBeEmpty)

        self.m_group = group

        self.m_group.SetGroupFlags(
            m_group.GetGroupFlags() | Box2D.b2_particleGroupCanBeEmpty)

    def GetGroup(self):
        return self.m_group

    def Step(self, dt, particleIndices, particleIndicesCount):
        numberOfParticlesCreated = 0
        self.m_emitRemainder += self.m_emitRate * dt

        pd = b2ParticleDef()
        pd.color = self.m_color
        pd.flags = self.m_flags
        pd.group = self.m_group

        while (self.m_emitRemainder > 1.0):
            self.m_emitRemainder -= 1.0
            angle = random.random() * 2.0 * Box2D.b2_pi
            distance = random.random()
            positionOnUnitCircle = b2Vec2(math.sin(angle), math.cos(angle))

            pd.position.Set(
                self.m_origin.x + positionOnUnitCircle.x * distance * self.m_halfSize.x,
                self.m_origin.y + positionOnUnitCircle.y * distance * self.m_halfSize.y)

            pd.velocity = self.m_startingVelocity
            if (self.m_speed != 0.0):
                pd.velocity += positionOnUnitCircle * self.m_speed

            particleIndex = self.m_particleSystem.CreateParticle(pd)
            if (self.m_callback != None):
                self.m_callback.ParticleCreated(
                    self.m_particleSystem, particleIndex)

            if (particleIndices and numberOfParticlesCreated < particleIndicesCount):
                particleIndices[numberOfParticlesCreated] = particleIndex

            numberOfParticlesCreated += 1

        return numberOfParticlesCreated


class MultipleParticleSystems (Framework):
    name = "MultipleParticleSystems Test"
    description = ''

    m_linear = False
    k_maxParticleCount = 500
    k_dynamicBoxSize = b2Vec2(0.5, 0.5)
    k_boxMass = 1.0
    k_emitRate = 100.0
    k_emitterPosition = b2Vec2(-5.0, 4.0)
    k_emitterVelocity = b2Vec2(7.0, -4.0)
    k_emitterSize = b2Vec2(1.0, 1.0)
    k_leftEmitterColor = b2ParticleColor(0x22, 0x33, 0xff, 0xff)
    k_rightEmitterColor = b2ParticleColor(0xff, 0x22, 0x11, 0xff)

    def __init__(self):
        super(MultipleParticleSystems, self).__init__()

        # Configure the default particle system's parameters.
        self.particleSystem.SetRadius(0.05)
        self.particleSystem.SetMaxParticleCount(self.k_maxParticleCount)
        self.particleSystem.SetDestructionByAge(True)

        # Create a secondary particle system.
        particleSystemDef = b2ParticleSystemDef()
        particleSystemDef.radius = self.particleSystem.GetRadius()
        particleSystemDef.destroyByAge = True

        self.particleSystem2 = self.world.CreateParticleSystem(
            particleSystemDef)
        self.particleSystem2.SetMaxParticleCount(self.k_maxParticleCount)

        # Don't restart the test when changing particle types.
        # TestMain:: SetRestartOnParticleParameterChange(false)

        # Create the ground.
        bd = b2BodyDef()
        ground = self.world.CreateBody(bd)
        shape = b2PolygonShape()
        shape.SetAsBox(5.0, 0.1)
        ground.CreateFixture(b2FixtureDef(shape=shape, density=0.0))

        # Create a dynamic body to push around.
        bd = b2BodyDef()
        bd.type = Box2D.b2_dynamicBody
        body = self.world.CreateBody(bd)
        shape = b2PolygonShape()
        center = b2Vec2(0.0, 1.2)
        shape.SetAsBox(self.k_dynamicBoxSize.x,
                       self.k_dynamicBoxSize.y, center, 0.0)
        body.CreateFixture(b2FixtureDef(shape=shape, density=0.0))
        massData = b2MassData()
        massData.mass = self.k_boxMass
        massData.center = center
        massData.I = 0.0
        body.massData = massData

        self.m_emitters = [RadialEmitter(), RadialEmitter()]

        self.setZoom(50.0)

        # Initialize the emitters.
        for i in range(0, 2):
            mirrorAlongY = 1.0
            if i & 1:
                mirrorAlongY = -1.0

            emitter = self.m_emitters[i]
            emitter.SetPosition(
                b2Vec2(self.k_emitterPosition.x * mirrorAlongY, self.k_emitterPosition.y))
            emitter.SetSize(self.k_emitterSize)
            emitter.SetVelocity(
                b2Vec2(self.k_emitterVelocity.x * mirrorAlongY, self.k_emitterVelocity.y))
            emitter.SetEmitRate(self.k_emitRate)

            if i & 1:
                emitter.SetColor(self.k_rightEmitterColor)
                emitter.SetParticleSystem(self.particleSystem2)
            else:
                emitter.SetColor(self.k_leftEmitterColor)
                emitter.SetParticleSystem(self.particleSystem)

    def Step(self, settings):
        dt = 1.0 / settings.hz
        super(MultipleParticleSystems, self).Step(settings)
        for i in range(0, 2):
            self.m_emitters[i].Step(dt, None, 0)


if __name__ == "__main__":
    main(MultipleParticleSystems)
